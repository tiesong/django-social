# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime

from django.contrib.auth.models import User
from news.models import News
from .models import Profile, Tag
from django.db.models import Q

# Create your views here.
def index(request):
	return HttpResponse("Hello world")

def people_list(request):
	navbar_pages = News.objects.filter(display_in_navbar=True)
	user_list = User.objects.all()
	tag_list = Tag.objects.all()

	context = {
		'user_list': user_list,
		'navbar_pages': navbar_pages,
		'tag_list': tag_list,
	}
	return render(request, 'community/people_list.html', context)

@login_required
def update(request):
    page_number = request.GET.get('pg_num', 0)

    user_list = User.objects.all()
    per = Paginator(user_list, 5)
    try:
        per_page = per.page(int(page_number))
        print('per page;{}'.format(per_page))

    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'user_list': False,
        }
        return render(request, 'community/people_list_content.html', context)

    context = {
        'user_list': per_page,
    }
    return render(request, 'community/people_list_content.html', context)

@login_required
def category(request):
    tag_name = request.GET.get('category')
    page_number = request.GET.get('pg_num', 0)
    tag_name = str(tag_name).replace("-", " ")
    profile_ids = Profile.objects.filter(tags__tag=tag_name).values_list('user', flat=True)
    user_list = User.objects.filter(id__in=set(profile_ids))

    per = Paginator(user_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'user_list': False,
        }
        return render(request, 'community/people_list_content.html', context)

    context = {
        'user_list': per_page,
    }
    return render(request, 'community/people_list_content.html', context)


@login_required
def search(request):
	keyword = request.GET.get('keyword', "")
	page_number = request.GET.get('pg_num', 0)
	keyword = str(keyword).replace("-", " ")
	user_list = User.objects.filter(Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))

	user_ids = Profile.objects.filter(Q(tags__tag__icontains=keyword) | Q(companies__name__icontains=keyword)).values_list('user', flat=True)
	profile_list = User.objects.filter(id__in=set(user_ids))

	user_list = user_list | profile_list

	per = Paginator(user_list, 5)

	try:
		per_page = per.page(int(page_number))
	except Exception as e:
		print('Error: {}'.format(e))
		context = {
			'user_list': False,
		}
		return render(request, 'community/people_list_content.html', context)

	context = {
		'user_list': per_page,
	}
	return render(request, 'community/people_list_content.html', context)

def profile(request, profile_id):
	user = User.objects.get(pk=profile_id)
	navbar_pages = News.objects.filter(display_in_navbar=True)
	profile = Profile.objects.filter(user=user).first()
	try:
		cats = profile.tags.all()
	except:
		cats = []

	context = {
		'user': user,
		'cats': cats,
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
