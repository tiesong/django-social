# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-21 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officespace', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='tiem_end',
            new_name='time_end',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='tiem_start',
            new_name='time_start',
        ),
    ]
