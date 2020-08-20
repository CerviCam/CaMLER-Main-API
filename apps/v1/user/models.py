from django.db import models
from apps.v1.common.models import BaseModel
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Degree(BaseModel):
    basemodel_ptr = models.OneToOneField(
        to = BaseModel,
        parent_link = True,
        related_name = "+",
        on_delete = models.CASCADE
    )

    instance_name = models.CharField(verbose_name = "Instance name", max_length = 255, blank=True)
    name = models.CharField(verbose_name = "Name", max_length = 255, blank=True)

    def __str__(self):
        return self.name

class Place(BaseModel):
    basemodel_ptr = models.OneToOneField(
        to = BaseModel,
        parent_link = True,
        related_name = "+",
        on_delete = models.CASCADE
    )

    country = models.CharField(verbose_name = "Country", max_length = 50, blank=True)
    province = models.CharField(verbose_name = "Province", max_length = 50, blank=True)
    city = models.CharField(verbose_name = "City", max_length = 50, blank=True)
    street_name = models.CharField(verbose_name = "Street name", max_length = 50, blank=True)
    postal_code = models.CharField(verbose_name = "Postal code", max_length = 6, blank=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self.street_name,
            self.city,
            self.province,
            self.country,
            self.postal_code
        )

class User(BaseModel):
    basemodel_ptr = models.OneToOneField(
        to = BaseModel,
        parent_link = True,
        related_name = "+",
        on_delete = models.CASCADE
    )

    name = models.CharField(verbose_name = "Name", max_length = 255)
    
    class Gender(models.IntegerChoices):
        MALE = 0, _('Male')
        FEMALE = 1, _('Female')
        UNKNOWN = 99, _('Unknown')
    gender = models.IntegerField(
        verbose_name= 'Gender',
        choices = Gender.choices,
        default = Gender.UNKNOWN,
    )

    account = models.OneToOneField(
        DjangoUser,
        verbose_name = "Account",
        on_delete = models.CASCADE,
    )
    degree = models.ForeignKey(
        Degree,
        verbose_name = "Degree",
        on_delete = models.SET_NULL,
        null = True,
    )
    workplace = models.OneToOneField(
        Place,
        verbose_name = "Workplace",
        on_delete = models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.name

@receiver(post_delete, sender=User)
def delete_relationship_fields(sender, instance, *args, **kwargs):
    if instance == None: return

    instance.account.delete()

    if instance.degree != None:
        instance.degree.delete()

    if instance.workplace != None:
        instance.workplace.delete()