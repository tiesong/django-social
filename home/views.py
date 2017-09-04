# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from news.models import News, Category

# Create your views here.
def index(request):
    
    try:
        feature_list = News.objects.order_by('-pub_date').order_by('-feature_rank')[0]
    except:
        feature_list = False

    email = password = ''
    if request.POST:
        logout(request)
        email = request.POST['login-email']
        password = request.POST['login-password']

        try:
            username = User.objects.get(email=email.lower()).username
        except:
            #no username found in system
            return HttpResponseRedirect('/error')

        try:
            user = authenticate(username=username, password=password)
        except:
            return HttpResponseRedirect('/error')

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/news/')
        else:
            #user is not in the system
            return HttpResponseRedirect('/error')

  
    context = {
        'feature_list': feature_list,
    }

    return render(request, 'home/index.html', context)

def error(request):
    message = "Sorry, your username and/or password were incorrect. Please go back and try again."
    context = {
        'message': message,
    }
    return render(request, 'home/error.html', context)