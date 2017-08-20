# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime

from django.contrib.auth.models import User

# Create your views here.
def index(request):
	return HttpResponse("Hello world")

def profile(request, profile_id):
	context = {}
	return render(request, 'people/profile.html', context)