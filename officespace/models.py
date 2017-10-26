# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
ROOM_TYPE = [('Meeting Space', 'Meeting Space'), ('Teleconference Room', 'Teleconference Room'),
             ('Workspaces', 'Workspaces'), ('Misc', 'Misc')]


class Room(models.Model):
    name = models.CharField(max_length=150, )
    category = models.CharField(max_length=100, choices=ROOM_TYPE, default='Meeting Space')
    
    def __str__(self):
        return self.name


class Booking(models.Model):
    room = models.ForeignKey(Room)
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    start_book = models.DateTimeField('start time')
    end_book = models.DateTimeField('end time')
    
    def __str__(self):
        return str(self.room)
