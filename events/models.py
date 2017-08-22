# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models


# Need to update settings.py to manage media files

class Event(models.Model):
    # need to add author relationship
    # need to add tagssssssss
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='event_images/%Y/%m/%d/', null=True, blank=True)
    start_date = models.DateTimeField('start date')

    pub_date = models.DateTimeField('date published')
    featured = models.BooleanField(default=False)

    def is_in_future(self):
        return self.start_date >= datetime.datetime.now()

    def __str__(self):
        return self.title
