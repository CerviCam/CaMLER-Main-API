import os
import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator

from apps.v1.common.models import BaseModel
from apps.v1.user.models import User
from apps.v1.common.tools import get_default_file_name_format, move_file, rename_file_name

# Create your models here.
class CervicClassification(BaseModel):
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    image = models.ImageField(upload_to = get_default_file_name_format("classifications"))
    
    class Status(models.IntegerChoices):
        WAITING = 0, _('Waiting')
        DONE = 1, _('Done')
    status = models.IntegerField(
        choices = Status.choices,
        default = Status.WAITING,
    )

    class Result(models.IntegerChoices):
        UNCLASSIFIED = 0, _('Unclassified')
        NEGATIVE = 1, _('Negative')
        POSITIVE = 2, _('Positive')
        UNKNOWN = 3, _('Unknown')
    result = models.IntegerField(
        choices = Result.choices,
        default = Result.UNCLASSIFIED,
    )

    def __str__(self):
        identity_name = os.path.basename(self.image.url)
        if self.creator != None:
            identity_name = self.creator.name

        return "{} [{}] [{}]".format(identity_name, self.get_status_display(), self.get_result_display())

@receiver(post_delete, sender = CervicClassification)
def post_delete_cervic_classification(sender, instance, *args, **kwargs):
    if instance == None: return

    image_path = instance.image.path
    if os.path.isfile(image_path):
        os.remove(image_path)

@receiver(pre_save, sender = CervicClassification)
def pre_save_cervic_classification(sender, instance, *args, **kwargs):
    if instance == None: return

    try:
        old_instance = CervicClassification.objects.get(id = instance.id)
        old_image_path = old_instance.image.path
        if old_instance.image != instance.image and os.path.isfile(old_image_path):
            os.remove(old_image_path)
    except CervicClassification.DoesNotExist:
        pass

@receiver(post_save, sender=CervicClassification)
def post_save_cervic_classification(sender, instance, *args, **kwargs):
    # Don't send a request if had been classified before
    if instance.status == CervicClassification.Status.DONE:
        return

    try:
        # Send classification request to AI API
        with open(instance.image.path, 'rb') as image:
            response = requests.post(
                '{}/predict'.format(settings.APIS['AI']['DOMAIN']),
                files = {
                    # 'debug': 'heloo'
                    'image': image,
                },
            )
        instance.status = CervicClassification.Status.DONE
        
        payload = response.json()
        if payload['result']['code'] == 0:
            instance.result = CervicClassification.Result.NEGATIVE
        elif payload['result']['code'] == 1:
            instance.result = CervicClassification.Result.POSITIVE
        else:
            instance.result = CervicClassification.Result.UNKNOWN
    except Exception:
        instance.result = CervicClassification.Result.UNKNOWN
    finally:
        instance.save()

def get_ai_model_name(instance, file_name):
    if instance.is_chosen:
        prefix = "chosen_"
    else:
        prefix = ""

    ext = file_name.split('.')[-1]
    return os.path.join("models/", "{}{}.{}".format(prefix, instance.name, ext))

def rename_model_name(instance, new_name):
    return rename_file_name(
        instance,
        "model",
        "{}.{}".format(new_name, instance.model.name.split(".")[-1]),
        should_save = False,
    )

class AIModel(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex='^\w+$',
                message='Must contain at least one of alphanumeric or underscore characters',
            ),
            RegexValidator(
                regex='^(?!.*((?i)chosen)).*',
                message='You can\'t name the model starts with "chosen"',
            ),
        ]
    )
    model = models.FileField(
        upload_to=get_ai_model_name,
        validators=[
            FileExtensionValidator(allowed_extensions=['pt'])
        ]
    )
    is_chosen = models.BooleanField(default=False)

    def __str__(self):
        if self.is_chosen:
            return "{} [CHOSEN]".format(self.name)
        return self.name

    def save(self, *args, **kwargs):
        try:
            # Get old instance
            old_instance = AIModel.objects.get(id = self.id)

            if old_instance.name != self.name and os.path.exists(self.model.path):
                rename_model_name(self, self.name)

        except AIModel.DoesNotExist:
            pass

        # Make sure only one object has is_chosen value to be True or none of AI models have that
        if self.is_chosen and "chosen" not in self.model.name:
            if os.path.exists(self.model.path):
                rename_model_name(self, "chosen_{}".format(self.name))

            for ai_model in AIModel.objects.all():
                if ai_model.is_chosen and self != ai_model:
                    rename_model_name(ai_model, self.name)
                    ai_model.is_chosen = False
                    ai_model.save()
        elif not self.is_chosen and self.name not in self.model.name:
            if os.path.exists(self.model.path):
                rename_model_name(self, self.name)
                
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "AI Model"
        verbose_name_plural = "AI Models"

@receiver(pre_save, sender=AIModel)
def pre_save_ai_model(sender, instance, *args, **kwargs):
    try:
        # Get old instance
        old_instance = AIModel.objects.get(id = instance.id)

        # Delete old model from storage if there is new model
        old_model_path = old_instance.model.path
        if old_instance.model != instance.model and os.path.isfile(old_model_path):
            os.remove(old_model_path)

    except AIModel.DoesNotExist:
        pass

@receiver(post_delete, sender = AIModel)
def post_delete_ai_model(sender, instance, *args, **kwargs):
    model_path = instance.model.path
    if os.path.isfile(model_path):
        os.remove(model_path)
