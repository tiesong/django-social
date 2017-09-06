# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    admin = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag = models.CharField(max_length=150)

    def __str__(self):
        return self.tag

# Need to update settings.py to manage media files
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tagline = models.CharField(max_length=155, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', null=True, blank=True)

    phone_number = models.CharField(max_length=30, blank=True, null=True, default=None)

    website = models.CharField(max_length=155, blank=True, null=True)
    twitter = models.CharField(max_length=155, blank=True, null=True)
    facebook = models.CharField(max_length=155, blank=True, null=True)
    linkedin = models.CharField(max_length=155, blank=True, null=True)

    bio = HTMLField(blank=True)

    companies = models.ManyToManyField(Company, blank=True)

    def __str__(self):
        return self.user.username
