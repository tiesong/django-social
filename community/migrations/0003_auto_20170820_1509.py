# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-20 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20170820_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
