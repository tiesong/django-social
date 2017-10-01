# Create your views here.
import json

from django.db.models import Q
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

    event_list = Event.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))\
        .order_by('start_date').distinct()

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
    days = False
    try:
        next_url = request.GET['next']
    except:
        next_url = False

    if request.POST:

        event_id = request.POST.get("event_id", "")
        event = Event.objects.filter(id=event_id).get()
        days = get_timedelta(event.pub_date, event.start_date)
        navbar_pages = News.objects.filter(display_in_navbar=True)

        context = {
            'event': event,
            'navbar_pages': navbar_pages,
            'next': next_url,
            'days': days
        }

        return render(request, 'events/event-details.html', context)

    if notify_id:
        Notification.objects.filter(id=notify_id).update(unread=0)
        return redirect('/events/' + event_id)

    navbar_pages = News.objects.filter(display_in_navbar=True)
    event = Event.objects.get(id=event_id)
    days = get_timedelta(event.pub_date, event.start_date)
    
    context = {
        'event': event,
        'navbar_pages': navbar_pages,
        'next': next_url,
        'days': days
    }
    return render(request, 'events/event-details.html', context)


def get_timedelta(pub_date, start_date):
    if pub_date - start_date < timedelta(days=1):
        return True
    else:
        return False
    
    
@login_required
def addNotify(request, event_id):

    if request.POST:
        user = User.objects.filter(username=request.user.username).get()

        event_id = request.POST.get("event_id", "")

        event = Event.objects.filter(id=event_id).get()

        description = "This Event will happen at " + str(event.start_date)

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
    try:
        next_url = request.GET['next']
        dashboard = True
    except:
        next_url = False
        dashboard = False

    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'navbar_pages': navbar_pages,
        'next': next_url,
        'dashboard': dashboard,
    }

    if request.POST:
        event_id = request.POST.get("event_id", None)

        title = request.POST.get("title", None)
        start_time = request.POST.get("startdatetime", None)
        start_date = dateutil.parser.parse(start_time)
        # start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M (%Z)')

        pub_time = request.POST.get("enddatetime", None)
        pub_date = dateutil.parser.parse(pub_time)
        # pub_date = datetime.strptime(pub_time, '%Y-%m-%d %H:%M (%Z)')

        event_url = request.POST.get("event-url", None)
        body = request.POST.get('body', '')

        if event_id:
            try:
                Event.objects.filter(id=event_id).update(author=request.user, title=title, start_date=start_time,
                                                         pub_date=pub_time, event_url=event_url, description=body)

            except Exception as e:
                print('Error : {}'.format(e))

            return redirect('/events/' + event_id)

        else:
            new_event = Event(author=request.user, title=title, start_date=start_date,
                              pub_date=pub_date, event_url=event_url, description=body)
            new_event.save()

            context = {
                'event': new_event,
                'navbar_pages': navbar_pages,
                'next': next_url,
                'dashboard': dashboard,
            }
            if next_url:
                return redirect(next_url+'/events')
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
    if not request.user.is_superuser:
        if not event_detail.author:
            return redirect('detail', event_id=event_id)
        elif (request.user.id != event_detail.author.id):
            return redirect('detail', event_id=event_id)
    try:
        next_url = request.GET['next']
    except:
        next_url = False

    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'event': event_detail,
        'navbar_pages': navbar_pages,
        'next': next_url,
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

            Event.objects.filter(id=event_id).update(description=body, author=request.user, title=title, start_date=start_date,
                                                     pub_date=pub_date,
                                                     event_url=event_url)

        except Exception as e:
            print('Error : {}'.format(e))

        if next_url:
            return redirect(next_url+'/events')
        else:
            return redirect('/events/' + event_id)

    return render(request, 'events/event-edit.html', context=context)


@login_required
def delete(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()

    context = {}

    return redirect('/dashboard/events')
