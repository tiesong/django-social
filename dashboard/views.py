# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from news.models import News
from perks.models import Perks


def index(request):
	news_list = News.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/content_dashboard.html', context)

def perks(request):
	news_list = Perks.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/perks_dashboard.html', context)


def users(request):
	user_list = User.objects.all()
	context = {
		'user_list': user_list,
	}
	return render(request, 'dashboard/users_dashboard.html', context)