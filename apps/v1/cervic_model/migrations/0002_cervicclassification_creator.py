# Generated by Django 3.0.8 on 2020-07-23 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200719_2031'),
        ('cervic_model', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cervicclassification',
            name='creator',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User'),
        ),
    ]