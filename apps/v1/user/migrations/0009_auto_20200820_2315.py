# Generated by Django 3.0.8 on 2020-08-20 16:15

from django.db import migrations

map_to_new = {
    0: 99,
    1: 0,
    2: 1,
}

map_to_old = {v: k for k, v in map_to_new.items()}

def map_gender_code(map):
    def change_gender_code(apps, schema_editor):
        User = apps.get_model('user', 'User')
        
        for instance in User.objects.all():
            instance.gender = map.get(instance.gender, instance.gender)
            instance.save()

    return change_gender_code

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200820_2314'),
    ]

    operations = [
        migrations.RunPython(
            map_gender_code(map_to_new),
            map_gender_code(map_to_old),
        )
    ]
