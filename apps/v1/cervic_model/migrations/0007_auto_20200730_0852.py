# Generated by Django 3.0.8 on 2020-07-30 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cervic_model', '0006_auto_20200730_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cervicclassification',
            name='result',
        ),
        migrations.RemoveField(
            model_name='cervicclassification',
            name='status',
        ),
    ]