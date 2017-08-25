# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Room, Booking

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'owner', 'title', 'start_book', 'end_book',)
