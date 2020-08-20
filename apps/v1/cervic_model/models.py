import os
import requests
import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator

from apps.v1.common.models import BaseModel
from apps.v1.user.models import User
from apps.v1.common.tools import DefaultFileNameFormat, move_file, rename_file_name
from datetime import datetime

# Create your models here.
class CervicClassification(BaseModel):
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    image = models.ImageField(upload_to = DefaultFileNameFormat(prefix="classifications"))
    
    class Status(models.IntegerChoices):
        WAITING = 0, _('Waiting')
        DONE = 1, _('Done')
    status = models.IntegerField(
        choices = Status.choices,
        default = Status.WAITING,
    )

    class Result(models.IntegerChoices):
        NEGATIVE = 0, _('Negative')
        POSITIVE = 1, _('Positive')
        UNKNOWN = 98, _('Unknown')
        UNCLASSIFIED = 99, _('Unclassified')
    result = models.IntegerField(
        choices = Result.choices,
        default = Result.UNCLASSIFIED,
    )

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

def classify_instance(instance):
    try:
        # Send classification request to AI API
        with open(instance.image.path, 'rb') as image:
            response = requests.post(
                '{}/predict'.format(settings.APIS['AI']['DOMAIN']),
                files = {
                    'image': image,
                },
            )
        instance.status = CervicClassification.Status.DONE
        
        payload = response.json()
        if payload['class'] == 0:
            instance.result = CervicClassification.Result.NEGATIVE
        elif payload['class'] == 1:
            instance.result = CervicClassification.Result.POSITIVE
        else:
            instance.result = CervicClassification.Result.UNKNOWN
    except Exception:
        instance.result = CervicClassification.Result.UNKNOWN
    finally:
        instance.save()

@receiver(post_save, sender=CervicClassification)
def post_save_cervic_classification(sender, instance, *args, **kwargs):
    # Don't send a request if had been classified before
    if instance.status == CervicClassification.Status.DONE:
        return

    classify_instance(instance)

def get_ai_model_name(instance, file_name):
    ext = file_name.split('.')[-1]
    return os.path.join("models/", "{}.{}".format(instance.name, ext))

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
        ]
    )
    model = models.FileField(
        upload_to=get_ai_model_name,
        validators=[
            FileExtensionValidator(allowed_extensions=['pt'])
        ]
    )
    is_chosen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            # Get old instance
            old_instance = AIModel.objects.get(id = self.id)

            if old_instance.name != self.name and os.path.exists(self.model.path):
                rename_model_name(self, self.name)

            no_one_is_chosen = True
            if self.is_chosen:
                # Make sure only one object has is_chosen value to be True
                for ai_model in AIModel.objects.all():
                    if ai_model.is_chosen and self != ai_model:
                        no_one_is_chosen = False
                        ai_model.is_chosen = False
                        ai_model.save()

            if old_instance.model.path != self.model.path or old_instance.is_chosen != self.is_chosen:
                config_path = os.path.join(settings.MEDIA_ROOT, "models/.config.json")
                
                # Create config file if doesn't exist
                if not os.path.exists(config_path):
                    with open(config_path, 'w') as config_file:
                        config_file.write("{}")

                with open(config_path, 'r+') as config_file:
                    config = json.load(config_file)

                    # Choose this model if chosen
                    if self.is_chosen:
                        config["chosen"] = os.path.basename(self.model.path)
                    elif no_one_is_chosen:
                        config["chosen"] = None
                
                    # Save new configuration
                    config_file.seek(0)
                    json.dump(config, config_file, indent=4)

                    # Remove remaining parts
                    config_file.truncate()

                        
        except AIModel.DoesNotExist:
            pass

                
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
    # Delete model file to free space
    model_path = instance.model.path
    if os.path.isfile(model_path):
        os.remove(model_path)
