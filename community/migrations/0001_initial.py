# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-13 19:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='Industry', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', tinymce.models.HTMLField(blank=True)),
                ('partner', models.BooleanField(default=False)),
                ('size', models.IntegerField(null=True)),
                ('website', models.CharField(blank=True, max_length=155, null=True)),
                ('twitter', models.CharField(blank=True, max_length=155, null=True)),
                ('facebook', models.CharField(blank=True, max_length=155, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=155, null=True)),
                ('categories', models.ManyToManyField(to='community.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tagline', models.CharField(blank=True, max_length=155, null=True)),
                ('advisor', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/%Y/%m/%d/')),
                ('phone_number', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('website', models.CharField(blank=True, max_length=155, null=True)),
                ('twitter', models.CharField(blank=True, max_length=155, null=True)),
                ('facebook', models.CharField(blank=True, max_length=155, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=155, null=True)),
                ('bio', tinymce.models.HTMLField(blank=True)),
                ('companies', models.ManyToManyField(blank=True, to='community.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='tags',
            field=models.ManyToManyField(blank=True, to='community.Tag'),
        ),
    ]