# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    logout(request)
    email = password = ''
    if request.POST:
        email = request.POST['login-email']
        password = request.POST['login-password']
        username = User.objects.get(email=email.lower()).username

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/news/')
  
    return render(request, 'home/index.html')