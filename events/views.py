# Create your views here.
from functools import wraps

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import dateutil.parser

from notifications.models import Notification
from .models import Event
from news.models import News
from django.contrib.auth.models import User
from notifications.signals import notify
from django.utils import timezone


def check_public(view_func):
    def _decorator(request, *args, **kwargs):
        event_id = kwargs['event_id']

        if not event_id:
            return HttpResponseRedirect('/')

        event_article = Event.objects.get(id=event_id)
        if event_article.public or request.user.is_authenticated():
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponseRedirect('/')

    return wraps(view_func)(_decorator)

# Create your views here.


def index(request):
    """
    Index
    :param request:
    :return:
    """

    week = int(request.GET.get('week_num', 0))
    event_list = Event.objects.order_by('start_date') if request.user.is_authenticated else \
        Event.objects.filter(public=True).order_by('start_date')
    
    event_all = Event.objects.all()
    user_all = User.objects.all().count()
    event_featured = Event.objects.filter(featured=True)
    event_count = len(event_all)
    navbar_pages = News.objects.filter(display_in_navbar=True)
    
    if len(event_list):
        
        base_date = timezone.now()
        print(base_date)
        limit_date = timezone.now() + timedelta(7)
        if request.user.is_authenticated:
            event_list_filter = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
                'start_date')
        else:
            event_list_filter = Event.objects.filter(public=True).filter(start_date__gte=base_date).filter(
                start_date__lte=limit_date).order_by(
                'start_date')
        event_top_list = Event.objects.all().order_by('-start_date')[1:3]
    
        context = {

            'event_top_list': event_top_list,
            'event_all': event_list_filter,
            'event_featured': event_featured,
            'event_count': event_count,
            'user_all': user_all,
            'navbar_pages': navbar_pages,
            'previous_page': True if base_date > event_list[0].start_date else False,
            'next_page': True if limit_date < event_list[len(event_list) - 1].start_date else False
            
        }
    else:
        context = {

            'event_top_list': False,
            'event_all': False,
            'event_featured': event_featured,
            'event_count': event_count,
            'user_all': user_all,
            'navbar_pages': navbar_pages,
            'next_page': False,
            'previous_page': False
        
        }

    return render(request, 'events/event-list.html', context)


def new(request):
    base_date = timezone.now()
    limit_date = timezone.now() + timedelta(7)
    if request.user.is_authenticated:
        event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
            '-start_date')
    else:
        event_list = Event.objects.filter(public=True).filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
            '-start_date')
        
    if len(event_list):
        context = {
            'event_all': event_list,
            'next_page': False,
            'previous_page': False
        }
    else:
        context = {
            'event_all': False,
            'next_page': False,
            'previous_page': False
        }
    return render(request, 'events/event-content.html', context)


def feature(request):
    week = int(request.GET.get('week_num', 0))

    event_list = Event.objects.filter(featured=True).order_by('start_date') if request.user.is_authenticated else \
                 Event.objects.filter(public=True).filter(featured=True).order_by('start_date')

    if len(event_list):
        base_date = event_list[0].start_date + timedelta(week * 7)
        limit_date = event_list[0].start_date + timedelta(7 + week * 7)
        if request.user.is_authenticated:
            event_list_filter = Event.objects.filter(featured=True).filter(start_date__gte=base_date).filter(
                start_date__lte=limit_date).order_by('start_date')
        else:
            event_list_filter = Event.objects.filter(public=True).filter(featured=True).filter(start_date__gte=base_date).filter(
                start_date__lte=limit_date).order_by('start_date')
        context = {
            'event_all': event_list_filter,
            'previous_page': True if base_date > event_list[0].start_date else False,
            'next_page': True if limit_date < event_list[len(event_list)-1].start_date else False
        }
    else:
        context = {
            'event_all': False,
            'next_page': False,
            'previous_page': False
        }
    return render(request, 'events/event-content.html', context)


def search(request):
    week = int(request.GET.get('week_num', 0))
    keyword = request.GET.get('keyword', "")
    keyword = str(keyword).replace("-", " ")
    if keyword == "":
        context = {
            'event_all': False
        }

        return render(request, 'events/event-content.html', context)
    
    if request.user.is_authenticated:
        event_list = Event.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))\
            .order_by('start_date').distinct()
    else:
        event_list = Event.objects.filter(public=True).filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)) \
            .order_by('start_date').distinct()
        
    if len(event_list):
        base_date = event_list[0].start_date + timedelta(week * 7)
        limit_date = event_list[0].start_date + timedelta(7 + week * 7)
        if request.user.is_authenticated:
            event_list_filter = Event.objects.filter(title__icontains=keyword).filter(start_date__gte=base_date) \
                .filter(start_date__lte=limit_date).order_by('start_date')
        else:
            event_list_filter = Event.objects.filter(public=True).filter(title__icontains=keyword).filter(start_date__gte=base_date) \
                .filter(start_date__lte=limit_date).order_by('start_date')
        context = {
            'event_all': event_list_filter,
            'previous_page': True if base_date > event_list[0].start_date else False,
            'next_page': True if limit_date < event_list[len(event_list) - 1].start_date else False
        }

    else:
        context = {
            'event_all': False,
            'next_page': False,
            'previous_page': False
        }

    return render(request, 'events/event-content.html', context)


def update(request):
    week = int(request.GET.get('week_num', 0))
    
    event_list = Event.objects.order_by('start_date') if request.user.is_authenticated \
        else Event.objects.filter(public=True).order_by('start_date')
    
    if len(event_list):
        base_date = timezone.now() + timedelta(week * 7)
        limit_date = timezone.now() + timedelta(7 + week * 7)
        
        if request.user.is_authenticated:
            event_list_filter = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
                'start_date')
        else:
            event_list_filter = Event.objects.filter(public=True).filter(start_date__gte=base_date).filter(
                start_date__lte=limit_date).order_by(
                'start_date')
        context = {
            'event_all': event_list_filter,
            'previous_page': True if base_date > event_list[0].start_date else False,
            'next_page': True if limit_date < event_list[len(event_list) - 1].start_date else False
        }

    else:
        context = {
            'event_all': False,
            'next_page': False,
            'previous_page': False
        }

    return render(request, 'events/event-content.html', context)


@check_public
def detail(request, event_id):
    """
    Event Detail.
    :param request:
    :param event_id:
    :return:
    """

    notify_id = request.GET.get('notify', None)
    try:
        next_url = request.GET['next']
    except Exception as e:
        print("Error: {}".format(e))
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
def addNotify(request):

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
    except Exception as e:
        print('Error: {}'.format(e))
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

        pub_time = request.POST.get("enddatetime", None)
        pub_date = dateutil.parser.parse(pub_time)

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
                return redirect(next_url + '/events')
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
        elif request.user.id != event_detail.author.id:
            return redirect('detail', event_id=event_id)
    try:
        next_url = request.GET['next']
    except Exception as e:
        print("Error: {}".format(e))
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

    return redirect('/dashboard/events')
