# Generated by Django 3.0.2 on 2020-03-30 00:15

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200111_2012'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, help_text='A short name that will be used to uniquely \t\tidentify you on the platform.', max_length=100, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Enter a valid username. This value must contain only letters, numbers, and the characters: @/./+/-/_ .', 'invalid')], verbose_name='Username'),
        ),
    ]
