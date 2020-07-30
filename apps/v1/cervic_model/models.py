import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

import os

from apps.v1.common.models import BaseModel
from apps.v1.user.models import User

def set_image_path(instance, file_name):
    ext = file_name.split('.')[-1]
    file_name = "images/{}.{}".format(timezone.now().strftime("%Y %m %d %H:%M:%S"), ext)
    return file_name

# Create your models here.
class CervicClassification(BaseModel):
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    image = models.ImageField(upload_to = set_image_path)
    
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
def delete_cervic_classification(sender, instance, *args, **kwargs):
    if instance == None: return

    image_path = instance.image.path
    if os.path.isfile(image_path):
        os.remove(image_path)

@receiver(pre_save, sender = CervicClassification)
def pre_save_cervic_classification(sender, instance, *args, **kwargs):
    if instance == None: return

    try:
        old_instance = CervicClassification.objects.get(id = instance.id)
    except CervicClassification.DoesNotExist:
        return False
        
    old_image_path = old_instance.image.path
    if old_instance.image != instance.image and os.path.isfile(old_image_path):
        os.remove(old_image_path)