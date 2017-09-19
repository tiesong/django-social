# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import News
from perks.models import Perks
from events.models import Event
from officespace.models import Room

@user_passes_test(lambda u: u.is_superuser)
def index(request):
	news_list = News.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/content_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def perks(request):
	news_list = Perks.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/perks_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
	user_list = User.objects.all()
	context = {
		'user_list': user_list,
	}
	return render(request, 'dashboard/users_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
	if request.POST:
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		try:
			exist_status = User.objects.filter(username=username).exists()
			if exist_status:
				context = { 'exist_status': exist_status, }
				return render(request, 'dashboard/users_create_dashboard.html', context)

			created_user = User.objects.create(username=username, email=email, password=password)
			user_list = User.objects.all()
			context = {
				'user_list': user_list,
				'created_user': created_user,
			}

			return render(request, 'dashboard/users_dashboard.html', context)
		except Exception as e:
			raise e

	return render(request, 'dashboard/users_create_dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def user_invitation(request):
	print ('Hello')

@user_passes_test(lambda u: u.is_superuser)
def events(request):
	event_list = Event.objects.all().order_by('-start_date')
	context = {
		'event_list': event_list,
	}
	return render(request, 'dashboard/events_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def rooms(request):
	room_list = Room.objects.all().order_by('category')
	context = {
		'room_list': room_list,
	}
	return render(request, 'dashboard/rooms_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def room_create(request):
	if request.POST:
		name = request.POST['name']
		category = request.POST['category']

		try:
			Room.objects.create(name=name, category=category)
			return redirect('/dashboard/rooms')
		except Exception as e:
			raise e

	categories = ['Meeting Space', 'Teleconference Room', 'Workspaces', 'Misc']
	context = {'categories': categories}

	return render(request, 'dashboard/rooms_create_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def room_edit(request, pk):
	room = Room.objects.get(pk=pk)
	categories = ['Meeting Space', 'Teleconference Room', 'Workspaces', 'Misc']

	context = {
		'room': room,
		'categories': categories,
	}

	if request.POST:
		name = request.POST['name']
		category = request.POST['category']

		try:
			room.name = name
			room.category = category
			room.save()

			return redirect('/dashboard/rooms')
		except Exception as e:
			raise e

	return render(request, 'dashboard/rooms_create_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def room_delete(request, pk):
	room = Room.objects.get(pk=pk)
	room.delete()
	context = {}
	return redirect('/dashboard/rooms')
