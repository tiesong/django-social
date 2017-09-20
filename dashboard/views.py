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
from community.models import Profile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

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
	user_list = Profile.objects.all()
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

			User.objects.create_user(username=username, email=email, password=make_password(password))
			user_list = Profile.objects.all()
			context = {
				'user_list': user_list,
			}

			return render(request, 'dashboard/users_dashboard.html', context)
		except Exception as e:
			raise e

	return render(request, 'dashboard/users_create_dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def user_invitation(request):
	to_email = request.GET['email']
	user_id = request.GET['user_id']
	username = request.GET['username']
	from_email = settings.DEFAULT_FROM_EMAIL
	subject = 'Invitation to join into York Butter Factory'
	message = 'Hi, \n\n\n' +\
	'This email is to help you join to York Butter Factory.\n\n'+\
	'Temporary account\n'+\
	'Username: '+ username +\
	'\nPasspord: password123\n\n'+\
	'Please click the ' + settings.SITE_URL + ' with the temporary infomation to continue to join us.\n'+\
	'To change the passowrd, please go to '+ settings.SITE_URL +'/password_reset.\n'+\
	'If clicking the links above does not work, please copy and paste the URL in a new browser window instead.\n\n\n'+\
	'Sincerely,\n'+\
	'The team at YBF'

	try:
		status = send_mail(subject, message, from_email, [to_email],)
		if status:
			Profile.objects.filter(pk=user_id).update(invitation_status=True)
			user_list = Profile.objects.all()
			context = {
				'user_list': user_list,
				'invitation_status': True,
				'invited_user': int(user_id),
			}
			return render(request, 'dashboard/users_dashboard.html', context)
	except Exception as e:
		raise e

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
