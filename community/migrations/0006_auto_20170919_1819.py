# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-19 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_profile_invitation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='invitation_status',
            field=models.BooleanField(default=True),
        ),
    ]
