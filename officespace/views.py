# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from .models import Room, Booking

# Create your views here.
def create(request):
    if request.GET.get('room_type'):
        room_type = request.GET['room_type']
        if room_type == 'meeting':
            cat = 'Meeting Space'
        elif room_type == 'tele':
            cat = 'Teleconference Room'
        elif room_type == 'work':
            cat = 'Workspaces'
        elif room_type == 'misc':
            cat = 'Misc'
        rooms = Room.objects.filter(category=cat)
    else:
        rooms = Room.objects.all()

    context = {
        'rooms': rooms,
    }

    if request.POST:
        owner = request.user
        room_id = request.POST['room_id']
        room = Room.objects.get(pk=room_id)
        date_start = request.POST['date_start']
        date_end = request.POST['date_end']

        try:
            Booking.objects.create(room=room, owner=owner, start_book=date_start, end_book=date_end)
            return HttpResponse('success')
        except:
            return HttpResponse('error')

    return render(request, 'officespace/create.html', context)

class BookingList(ListView):
    model = Booking
    template_name = 'officespace/bookings.html'

    def get_queryset(self):
        if self.request.GET.get('room_type'):
            room_type = self.request.GET['room_type']
            if room_type == 'meeting':
                cat = 'Meeting Space'
            elif room_type == 'tele':
                cat = 'Teleconference Room'
            elif room_type == 'work':
                cat = 'Workspaces'
            elif room_type == 'misc':
                cat = 'Misc'
            room = Room.objects.filter(category=cat)
            queryset = Booking.objects.filter(owner=self.request.user, room=room)
        else:
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
