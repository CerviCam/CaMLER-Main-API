# Generated by Django 3.0.8 on 2020-08-13 04:17
from django.db import migrations
import os
from apps.v1.common.tools import move_file
from django.conf import settings

OLD_LOCATION = "images/"
NEW_LOCATION = "classifications/"

def move_classification_images_to_new_location(new_location):
    def move_classification_images(apps, schema_editor):
        CervicClassification = apps.get_model('cervic_model', 'CervicClassification')
        
        for instance in CervicClassification.objects.all():
            new_name = os.path.join(new_location, os.path.basename(instance.image.name))
            new_path = os.path.join(
                settings.MEDIA_ROOT,
                new_name.strip("/").strip("\\"),
            )
            move_file(instance.image.path, new_path)
            instance.image.name = new_name
            instance.save()

    return move_classification_images

class Migration(migrations.Migration):
    dependencies = [
        ('cervic_model', '0008_auto_20200730_0854'),
    ]

    operations = [
        migrations.RunPython(
            move_classification_images_to_new_location(NEW_LOCATION),
            move_classification_images_to_new_location(OLD_LOCATION),
        ),
    ]