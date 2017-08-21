# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Need to update settings.py to manage media files

class Event(models.Model):
	#need to add author relationship
	#need to add tagssssssss
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='event_images/%Y/%m/%d/', null=True, blank=True)
    start_date = models.DateTimeField('start date', null=True, blank=True)
    end_date = models.DateTimeField('end date', null=True, blank=True)
    event_url = models.CharField(max_length=200, null=True, blank=True)
    featured = models.BooleanField(default=False)
    description = models.CharField(max_length=5000, null=True, blank=True)

    def is_in_future(self):
        return self.start_date >= datetime.now()

    def __str__(self):
    	return self.title

