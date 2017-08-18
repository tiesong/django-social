# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

#from .models import Event
from .models import Event

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
	'event_list': event_list
	}
	return render(request, 'events/event-list.html', context)

def detail(request, event_id):
	event = Event.objects.get(id=event_id)
	context={
	'event': event,
	}
	return render(request, 'events/event-details.html', context)