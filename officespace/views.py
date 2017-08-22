# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from .models import Room, Booking

# Create your views here.
class BookingCreate(CreateView):
    model = Booking
    template_name = 'officespace/create.html'
    success_url = reverse_lazy('booking_list')
    
class BookingList(ListView):
    model = Booking
    template_name = 'officespace/bookings.html'

    def get_queryset(self):
    	queryset = Booking.objects.filter(owner=self.request.user)
    	return queryset

class BookingUpdate(UpdateView):
    model = Booking
    template_name = 'officespace/edit.html'
    success_url = reverse_lazy('booking_list')

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')

class BookingDetail(DetailView):
    model = Booking
    template_name = 'officespace/detail.html'
