# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from .models import Room, Booking
from news.models import News
from django.contrib.auth.models import User
import json, datetime
from django.db.models import Q

# Create your views here.
navbar_pages = News.objects.filter(display_in_navbar=True)


def create(request):
    room_type = ''
    start_date = ''
    end_date = ''
    start_date_value = ''
    end_date_value = ''
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
        else:
            cat = 'all'

        if cat == 'all':
            rooms = Room.objects.filter()
        else:
            rooms = Room.objects.filter(category=cat)
    elif request.GET.get('room_id'):
        room_id = request.GET['room_id']
        print('room_id: {}'.format(room_id))
        start_book = request.GET['start_book']
        end_book = request.GET['end_book']
        room = Room.objects.get(pk=room_id)
        bookings = Booking.objects.filter(room=room)
        response = []
        for booking in bookings:
            if request.user == booking.owner:
                owner = 'true'
            else:
                owner = 'false'
            title = booking.title
            start_book = booking.start_book
            end_book = booking.end_book
            response.append([owner, title, start_book, end_book])
        response = json.dumps(response, default=datetime_handler)

        return HttpResponse(response)

    elif request.GET.get('type') == 'search':
        start_book = request.GET['date_start']
        end_book = request.GET['date_end']
        if start_book != '' and end_book != '':
            room_ids= Booking.objects.values_list('room__id', flat=True).filter(
                Q(start_book__gte=start_book, start_book__lt=end_book)
                | Q(end_book__gt=start_book, end_book__lte=end_book)
                | Q(start_book__gte=start_book, end_book__lte=end_book)
                | Q(start_book__lte=start_book, end_book__gte=end_book))
            rooms = Room.objects.filter(~Q(id__in=set(room_ids)))
            start_date = datetime.datetime.strptime(start_book,'%Y-%m-%d %H:%M').strftime('%I%p, %d %B %Y')
            start_date_value = start_book
            end_date = datetime.datetime.strptime(end_book,'%Y-%m-%d %H:%M').strftime('%I%p, %d %B %Y')
            end_date_value = end_book
        else:
            rooms = Room.objects.all()

    else:
        rooms = Room.objects.all()

    context = {
        'rooms': rooms,
        'room_type': room_type,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_value': start_date_value,
        'end_date_value': end_date_value,
        'navbar_pages': navbar_pages,
    }

    if request.POST:
        owner = request.user
        room_id = request.POST['room_id']
        room = Room.objects.get(pk=room_id)
        date_start = request.POST['date_start']
        date_end = request.POST['date_end']
        title = request.POST['title']

        try:
            booking = Booking.objects.create(room=room, owner=owner, title=title, start_book=date_start, end_book=date_end)
            response = []
            title = booking.title
            room = booking.room.name
            start_book = booking.start_book
            end_book = booking.end_book
            response = [room, title, start_book, end_book]
            response = json.dumps(response)

            return HttpResponse(response)
        except:
            return HttpResponse('error')

    return render(request, 'officespace/create.html', context)


def bookings(request):
    """
    Return bookings list
    :param request:
    :return:
    """
    if request.POST:
        room_ids = request.POST['room_id'].split(",")
        start_book = request.POST['start_book']
        end_book = request.POST['end_book']
        response = []
        
        if "all" in room_ids:  # select all
            room_ids = Room.objects.values_list('id', flat=True)
        elif "none" in room_ids:  # select none
            room_ids = []
        
        for room_id in room_ids:
            room = Room.objects.get(pk=room_id)
            bookings = Booking.objects.filter(room=room, owner=request.user)
            
            for booking in bookings:
                if request.user == booking.owner:
                    owner = 'true'
                else:
                    owner = 'false'
                title = booking.title
                start_book = booking.start_book
                end_book = booking.end_book
                response.append([owner, title, start_book, end_book])
        response = json.dumps(response, default=datetime_handler)
    
        return HttpResponse(response)
    else:
        date_start = request.GET['date_start']
        date_end = request.GET['date_end']
        print(date_start, date_end)
        bookings = Booking.objects.filter(Q(start_book__lte=date_end) & Q(start_book__gte=date_start)|
                                          Q(start_book__lte=date_start) & Q(end_book__gte=date_end)|
                                          Q(end_book__lte=date_end) & Q(end_book__gte=date_start))\
                                            .filter(owner=request.user)
                            
        available_room = []
        print('bookings:{}'.format(bookings))
        for item in bookings:
            if len(available_room) != 0:
                if {'id': item.room.id, 'name': item.room.name} in available_room:
                    continue
            available_room.append({'id': item.room.id, 'name': item.room.name})

        response = json.dumps(available_room, default=datetime_handler)
        print('response: {}'.format(response))
        return HttpResponse(response)
        
        
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
            else:
                cat = 'all'

            if cat == 'all':
                queryset = Booking.objects.filter(owner=self.request.user, start_book__gte=datetime.datetime.now()-datetime.timedelta(days=7))
            else:
                queryset = Booking.objects.filter(owner=self.request.user, room__category=cat, start_book__gte=datetime.datetime.now()-datetime.timedelta(days=7))
        else:
            queryset = Booking.objects.filter(owner=self.request.user, start_book__gte=datetime.datetime.now()-datetime.timedelta(days=7))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BookingList, self).get_context_data(**kwargs)
        if self.request.GET.get('room_type'):
            context['room_type'] = self.request.GET.get('room_type')
        context['navbar_pages'] = navbar_pages
        return context

def edit(request, pk):
    if request.GET:
        if request.GET.get('booking_id'):
            booking_id = request.GET['booking_id']
            room_id = request.GET['room_id']
            # start_book = request.GET['start_book']
            # end_book = request.GET['end_book']
            room = Room.objects.get(pk=room_id)
            bookings = Booking.objects.filter(room=room)
            response = []
            for booking in bookings:
                if booking.pk == int(pk):
                    editing = 'true'
                else:
                    editing = 'false'
                if booking.owner == request.user:
                    owner = 'true'
                else:
                    owner = 'false'
                title = booking.title
                start_book = booking.start_book
                end_book = booking.end_book
                response.append([owner, title, start_book, end_book, editing])
            response = json.dumps(response, default=datetime_handler)

            return HttpResponse(response)
        else:
            room_id = request.GET['room']
            rooms = Room.objects.all()

        context = {
            'rooms': rooms,
            'pk': pk,
            'room_id': room_id,
            'navbar_pages': navbar_pages,
        }

    if request.POST:
        owner = request.user
        booking_id = request.POST['booking_id']
        room_id = request.POST['room_id']
        room = Room.objects.get(pk=room_id)
        date_start = request.POST['date_start']
        date_end = request.POST['date_end']
        title = request.POST['title']

        try:
            booking = Booking.objects.filter(pk=booking_id).update(room=room, owner=owner, title=title, start_book=date_start, end_book=date_end)
            response = []
            title = title
            room = room.name
            start_book = date_start
            end_book = date_end
            response = [room, title, start_book, end_book]
            response = json.dumps(response)
            return HttpResponse(response)
        except:
            return HttpResponse('error')

    return render(request, 'officespace/edit.html', context)

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')

class BookingDetail(DetailView):
    model = Booking
    template_name = 'officespace/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookingDetail, self).get_context_data(**kwargs)
        context['navbar_pages'] = navbar_pages
        return context

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
