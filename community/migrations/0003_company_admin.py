# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-14 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0002_auto_20170913_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='admin',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
