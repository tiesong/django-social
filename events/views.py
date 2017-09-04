# Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import dateutil.parser

# from .models import Event
from .models import Event

# Create your views here.


@login_required
def index(request):

    current_day = datetime.now().strftime("%Y-%m-%d")
    print(current_day)
    event_all = Event.objects.all()
    event_featured = Event.objects.filter(featured=True)

    context = {
        'event_all': event_all,
        'current_day': current_day,
        'event_featured': event_featured
    }

    return render(request, 'events/event-list.html', context)


@login_required
def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'events/event-details.html', context)


@login_required
def create(request):
    """
    Create new event.
    :param request: 
    :return: 
    """

    event_id = request.POST.get("event_id", None)

    if event_id:

        try:
            body = request.POST.get('body', "")
            Event.objects.filter(id=event_id).update(description=body)

        except Exception as e:
            print('Error : {}'.format(e))

        return redirect('/events/' + event_id)

    else:
        title = request.POST.get("title", None)
        start_time = request.POST.get("startdatetime", None)
        start_date = dateutil.parser.parse(start_time)

        pub_time = request.POST.get("enddatetime", None)
        pub_date = dateutil.parser.parse(pub_time)

        event_url = request.POST.get("event-url", None)

        new_event = Event(title=title, start_date=start_date,
                          pub_date=pub_date, event_url=event_url, description="")
        new_event.save()

        context = {
            'event': new_event
        }

        return render(request, 'events/event-edit.html', context=context)


@login_required
def edit(request, event_id):
    """
    Edit Event
    :param request: 
    :param event_id: 
    :return: 
    """
    event_detail = Event.objects.get(id=event_id)

    context = {
        'event': event_detail
    }

    if request.POST:
        try:
            body = request.POST.get('body', "")
            Event.objects.filter(id=event_id).update(description=body)

        except Exception as e:
            print('Error : {}'.format(e))

        return redirect('/events/' + event_id)

    return render(request, 'events/event-edit.html', context=context)


@login_required
def delete(request):
    pass
