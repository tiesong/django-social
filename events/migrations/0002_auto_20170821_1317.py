# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-21 13:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='pub_date',
            new_name='end_date',
        ),
    ]
