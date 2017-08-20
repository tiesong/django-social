# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from news.models import News


def index(request):
	news_list = News.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/news_dashboard.html', context)
