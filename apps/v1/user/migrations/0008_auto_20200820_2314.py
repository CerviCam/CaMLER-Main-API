# Generated by Django 3.0.8 on 2020-08-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Male'), (1, 'Female'), (99, 'Unknown')], default=99, verbose_name='Gender'),
        ),
    ]
