# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('untitled', '0006_auto_20160219_2050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpage',
            old_name='timeCreated',
            new_name='time_created',
        ),
        migrations.RenameField(
            model_name='userpage',
            old_name='timeUpdated',
            new_name='time_updated',
        ),
    ]
