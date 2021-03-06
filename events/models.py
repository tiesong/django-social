# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
import datetime
from django.db import models
from django.contrib.auth.models import User


# Need to update settings.py to manage media files

class Event(models.Model):
    author = models.ForeignKey(User)
    # need to add tags
    title = models.CharField(max_length=150)
    # image = models.ImageField(upload_to='event_images/%Y/%m/%d/', null=True, blank=True)
    start_date = models.DateTimeField('start date', null=True)
    public = models.BooleanField(default=False)
    description = HTMLField(blank=True)
    featured_image = models.ImageField(upload_to='events_images/%Y/%m/%d/', null=True, blank=True)
    pub_date = models.DateTimeField('date published', null=True)
    featured = models.BooleanField(default=False)
    event_url = models.CharField(max_length=150, null=True)

    def is_in_future(self):
        return self.start_date >= datetime.datetime.now()

    def __str__(self):
        return self.title
