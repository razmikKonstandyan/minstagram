# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('untitled', '0002_k'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
