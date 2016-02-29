# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 13:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20160229_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiledata',
            name='subscriptions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='v', to=settings.AUTH_USER_MODEL),
        ),
    ]
