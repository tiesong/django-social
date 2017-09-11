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
from notifications.models import Notification

from .models import Event
from news.models import News
from django.contrib.auth.models import User
from notifications.signals import notify


# Create your views here.


@login_required
def index(request):
    """
    Index 
    :param request: 
    :return: 
    """

    week = int(request.GET.get('week_num', 0))
    next_week = week + 1
    previous_week = week - 1

    # this sets up for a 10 day event view window in the template
    base_date = datetime.now() + timedelta(week * 7)
    limit_date = datetime.now() + timedelta(7 + week * 7)

    event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
        'start_date')

    event_top_list = Event.objects.all().order_by('-start_date')[1:3]

    event_all = Event.objects.all()
    user_all = User.objects.all().count()
    event_featured = Event.objects.filter(featured=True)
    event_count = len(event_all)
    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'next_week': next_week,
        'previous_week': previous_week,
        'event_top_list': event_top_list,
        'event_all': event_list,
        'event_featured': event_featured,
        'event_count': event_count,
        'user_all': user_all,
        'navbar_pages': navbar_pages,
    }

    return render(request, 'events/event-list.html', context)


@login_required
def new(request):
    week = int(request.GET.get('week_num', 0))

    base_date = datetime.now()
    limit_date = datetime.now() + timedelta(7)

    event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
        'start_date')

    if len(event_list):

        context = {
            'event_all': event_list
        }

        return render(request, 'events/event-content.html', context)

    else:
        context = {
            'event_all': False
        }
        return render(request, 'events/event-content.html', context)


@login_required
def feature(request):
    week = int(request.GET.get('week_num', 0))

    event_list = Event.objects.filter(featured=True).order_by('start_date')

    if len(event_list):
        base_date = event_list[0].start_date + timedelta(week * 7)
        limit_date = event_list[0].start_date + timedelta(7 + week * 7)
        event_list = Event.objects.filter(featured=True).filter(start_date__gte=base_date).filter(
            start_date__lte=limit_date).order_by('start_date')
        context = {

            'event_all': event_list
        }

        return render(request, 'events/event-content.html', context)

    else:
        context = {
            'event_all': False
        }
        return render(request, 'events/event-content.html', context)


@login_required
def search(request):
    week = int(request.GET.get('week_num', 0))
    keyword = request.GET.get('keyword', "")
    keyword = str(keyword).replace("-", " ")
    if keyword == "":
        context = {
            'event_all': False
        }

        return render(request, 'events/event-content.html', context)

    event_list = Event.objects.filter(title__icontains=keyword).order_by('start_date')

    if len(event_list):
        base_date = event_list[0].start_date + timedelta(week * 7)
        limit_date = event_list[0].start_date + timedelta(7 + week * 7)

        event_list = Event.objects.filter(title__icontains=keyword).filter(start_date__gte=base_date) \
            .filter(start_date__lte=limit_date).order_by('start_date')

        context = {
            'event_all': event_list
        }

    else:
        context = {
            'event_all': False
        }

    return render(request, 'events/event-content.html', context)


@login_required
def update(request):
    week = int(request.GET.get('week_num', 0))

    base_date = datetime.now() + timedelta(week * 7)
    limit_date = datetime.now() + timedelta(7 + week * 7)

    event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
        'start_date')

    context = {
        'event_all': event_list
    }

    return render(request, 'events/event-content.html', context)


@login_required
def detail(request, event_id):
    """
    Event Detail.
    :param request: 
    :param event_id: 
    :return: 
    """
    notify_id = request.GET.get('notify', None)

    if request.POST:

        event_id = request.POST.get("event_id", "")
        event = Event.objects.filter(id=event_id).get()

        navbar_pages = News.objects.filter(display_in_navbar=True)

        context = {
            'event': event,
            'navbar_pages': navbar_pages,
        }

        return render(request, 'events/event-details.html', context)

    if notify_id:
        Notification.objects.filter(id=notify_id).update(unread=0)
        return redirect('/events/' + event_id)

    navbar_pages = News.objects.filter(display_in_navbar=True)
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
        'navbar_pages': navbar_pages,
    }
    return render(request, 'events/event-details.html', context)


@login_required
def addNotify(request, event_id):

    if request.POST:
        user = User.objects.filter(username=request.user.username).get()

        event_id = request.POST.get("event_id", "")

        event = Event.objects.filter(id=event_id).get()

        description = event.title + " will happen at " + str(event.start_date)

        notify.send(user, recipient=user, verb="Successfully set Reminder for",
                    target=event, description=description)

        return redirect('/events/' + event_id)


@login_required
def create(request):
    """
    Create new event.
    :param request: 
    :return: 
    """
    event_id = request.POST.get("event_id", None)
    navbar_pages = News.objects.filter(display_in_navbar=True)

    title = request.POST.get("title", None)
    start_time = request.POST.get("startdatetime", None)
    start_date = dateutil.parser.parse(start_time)

    pub_time = request.POST.get("enddatetime", None)
    pub_date = dateutil.parser.parse(pub_time)

    event_url = request.POST.get("event-url", None)

    if event_id:
        try:
            body = request.POST.get('body', "")
            Event.objects.filter(id=event_id).update(title=title, start_date=start_date,
                                                     pub_date=pub_date, event_url=event_url, description=body)

        except Exception as e:
            print('Error : {}'.format(e))

        return redirect('/events/' + event_id)

    else:

        new_event = Event(title=title, start_date=start_date,
                          pub_date=pub_date, event_url=event_url)
        new_event.save()

        context = {
            'event': new_event,
            'navbar_pages': navbar_pages,
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
    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'event': event_detail,
        'navbar_pages': navbar_pages,
    }

    if request.POST:
        try:
            body = request.POST.get('body', "")
            title = request.POST.get("title", None)
            start_time = request.POST.get("startdatetime", None)
            start_date = dateutil.parser.parse(start_time)

            pub_time = request.POST.get("enddatetime", None)
            pub_date = dateutil.parser.parse(pub_time)

            event_url = request.POST.get("event-url", None)

            Event.objects.filter(id=event_id).update(description=body, title=title, start_date=start_date,
                                                     pub_date=pub_date,
                                                     event_url=event_url)

        except Exception as e:
            print('Error : {}'.format(e))

        return redirect('/events/' + event_id)

    return render(request, 'events/event-edit.html', context=context)


@login_required
def delete(request):
    """
    Delete Event.
    :param request: 
    :return: 
    """
    pass
