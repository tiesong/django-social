# Create your views here.
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

    # Search
    if request.POST:
        keyword = request.POST.get('keyword', None)
        print(keyword)
        if keyword:
            event_list = Event.objects.filter(title__icontains=keyword)

            context = {
                'event_list': event_list
            }

    # week, category
    else:
        week = int(request.GET.get('week', 0))
        category = request.GET.get('category', None)

        # When New or Featured.
        if category:
            event_list = Event.objects.filter(featured=1)
            context = {
                'event_list': event_list
            }

        # When week.
        else:

            if week:
                next_week = week + 1
                previous_week = week - 1
            else:
                week = 0
                next_week = 1
                previous_week = -1

            # this sets up for a 10 day event view window in the template
            base_date = datetime.now() + timedelta(week * 10)
            limit_date = datetime.now() + timedelta(10 + week * 10)
            print(base_date, limit_date)
            event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
                'start_date')

            context = {
                'next_week': next_week,
                'previous_week': previous_week,
                'event_list': event_list
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
            print('Error')

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
def edit(request):

    if request.POST:
        pass


@login_required
def delete(request):
    pass
