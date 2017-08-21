# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
ROOM_TYPE = [('meeting_space', 'Meeting Space'), ('releconference_room', 'Teleconference Room'), ('workspaces', 'Workspaces'), ('misc', 'Misc')]
class Room(models.Model):
    name = models.CharField(max_length=150,)
    category = models.CharField(max_length=100, choices=ROOM_TYPE, default='Meeting Space')

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(Room)
    owner = models.ForeignKey(User)
    booked_date = models.DateField('date booked')
    time_start = models.TimeField('start time')
    time_end = models.TimeField('end time')

    def __str__(self):
    	return str(self.room)
