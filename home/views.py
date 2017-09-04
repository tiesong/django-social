# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from news.models import News, Category

# Create your views here.
def index(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/news')
    else:
        try:
            feature_list = News.objects.order_by('-pub_date').order_by('-feature_rank')[0]
        except:
            feature_list = False

        email = password = ''


        if request.POST:
            #collect all potential field inputs
            logout(request)
            email = request.POST['login-email']
            password = request.POST['login-password']

            try: #we try logging a user in first
                username = User.objects.get(email=email.lower()).username
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/news/')
                    else:
                        #user is not in the system
                        message = "Sorry, but we could not find your username in our system. Please try again."
                        request.session['error'] = message
                        return HttpResponseRedirect('/error')
            
            except: #if logging in fails, let's try signing them up
                request.session['error'] = "Sorry, the username / password combination could not be found. Please try again."
                return HttpResponseRedirect('/error')
      
        context = {
            'feature_list': feature_list,
        }

        return render(request, 'home/index.html', context)

def signup(request):
    try:
        if request.POST:
            signup_firstname = request.POST['signup-firstname']
            signup_lastname = request.POST['signup-lastname']
            signup_email = request.POST['signup-email']
            signup_password = request.POST['signup-password']

            user = User.objects.create_user(username=signup_email, first_name=signup_firstname, last_name=signup_lastname)
            login(request, user)
            return HttpResponseRedirect('/news/')
        else:
            return HttpResponseRedirect('/error')
    except: #if logging in fails, let's try signing them up
        return HttpResponseRedirect('/error')

def error(request):

    try:
        message = request.session['error']
        request.session['error'] = ''
    except:
        message = "Whoops. Something has gone wrong. Please try again or email nick@typehuman.com for help."
        request.session['error'] = ''
    
    context = {
        'message': message,
    }
    return render(request, 'home/error.html', context)