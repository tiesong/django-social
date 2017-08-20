# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .forms import EventForm
from datetime import datetime, timedelta
from .models import Event

from django.http import HttpResponseRedirect
from .forms import EventForm

import pdb

# Create your views here.

@login_required
def index(request):
	try:
		week=int(request.GET.get('week', ''))
		next_week=week+1
		previous_week=week-1
	except:
		week=0
		next_week=1
		previous_week=-1

	#this sets up for a 10 day event view window in the template
	base_date = datetime.now()+timedelta(week*10)
	limit_date = datetime.now()+timedelta(10+week*10)
	event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by('start_date')

	context = {
		'next_week': next_week,
		'previous_week': previous_week,
		'event_list': event_list,
		'form': EventForm()
	}
	return render(request, 'events/event-list.html', context)

def detail(request, event_id):
	event = Event.objects.get(id=event_id)
	context={
	'event': event,
	}
	return render(request, 'events/event-details.html', context)


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event(title=request.POST['event_name'], image='', start_date='2010-10-6', pub_date='2010-10-6', featured=True)
            event.save()
            return HttpResponseRedirect('show')
    else:
        form = EventForm()
    return render(request, 'events/events-detail.html', {'form': form})

def event_show(request):
	event_data = Event.objects.all()
	context = {
		'event_data': event_data,
	}
	return render(request, 'events/event_show.html', context)