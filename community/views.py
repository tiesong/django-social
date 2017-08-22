# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime

from django.contrib.auth.models import User
from news.models import News

# Create your views here.
def index(request):
	return HttpResponse("Hello world")

def people_list(request):
	navbar_pages = News.objects.filter(display_in_navbar=True)
	user_list = User.objects.all()

	context = {
		'user_list': user_list,
		'navbar_pages': navbar_pages,
	}
	return render(request, 'community/people_list.html', context)


def profile(request, profile_id):
	user = User.objects.get(pk=profile_id)
	navbar_pages = News.objects.filter(display_in_navbar=True)

	context = {
		'user': user,
		'navbar_pages': navbar_pages,
	}
	return render(request, 'community/profile.html', context)

def edit_profile(request, profile_id):
	user = User.objects.get(pk=profile_id)
	navbar_pages = News.objects.filter(display_in_navbar=True)

	context = {
		'user': user,
		'navbar_pages': navbar_pages,
	}
	return render(request, 'community/profile-edit.html', context)

def companies(request):
	navbar_pages = News.objects.filter(display_in_navbar=True)
	context = {
		'navbar_pages': navbar_pages,
	}
	return render(request, 'community/company.html', context)

def company(request, company_id):
	navbar_pages = News.objects.filter(display_in_navbar=True)
	context = {
		'navbar_pages': navbar_pages,
	}
	return render(request, 'community/company.html', context)