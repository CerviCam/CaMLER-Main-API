# Generated by Django 3.0.8 on 2020-07-31 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200719_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')], default=0, verbose_name='Gender'),
        ),
    ]
