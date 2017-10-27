# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from news.models import News, Category
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/officespace')
    else:
        active_status = request.GET.get('active', None)
        try:
            feature_list = News.objects.order_by('-pub_date').order_by('-feature_rank')[0]
        except:
            feature_list = False
        
        email = password = ''
        
        if request.POST:
            # collect all potential field inputs
            logout(request)
            email = request.POST['login-email']
            password = request.POST['login-password']
            print(email, password)
            try:  # we try logging a user in first
                username = User.objects.get(email=email.lower()).username
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/officespace/')
                    else:
                        # user is not in the system
                        request.session[
                            'error_message'] = "It looks like you're account has been deactivated. Please contact site admin for assistance."
                        return HttpResponseRedirect('/error?login=fail')
                else:
                    request.session[
                        'error_message'] = "Sorry, the username and/or password combination could not be found. Please try again."
                    return HttpResponseRedirect('/error?login=fail')
            
            except:  # if logging in fails, let's try signing them up
                request.session[
                    'error_message'] = "Sorry, the username and/or password combination could not be found. Please try again."
                return HttpResponseRedirect('/error?login=fail')
        
        if active_status is None:
            context = {
                'feature_list': feature_list,
                'active_status': True
            }
        else:
            context = {
                'feature_list': feature_list,
                'active_status': False
            }
        
        return render(request, 'home/index.html', context)


def signup(request):
    try:
        if request.POST:
            signup_firstname = request.POST['signup-firstname']
            signup_lastname = request.POST['signup-lastname']
            signup_email = request.POST['signup-email']
            signup_password = request.POST['signup-password']
            username = signup_firstname.lower() + signup_lastname.lower()
            if len(User.objects.filter(email=signup_email)) > 0:
                request.session[
                    'error_message'] = "A user already exists on the site with that email. Perhaps try logging in?"
                return HttpResponseRedirect('/error?signup=fail')
            else:
                user = User.objects.create_user(username=username, email=signup_email, first_name=signup_firstname,
                                                last_name=signup_lastname, password=signup_password)
                user.is_active = False
                user.save()
                login(request, user)
                
                send_email("User", username, signup_email)
                send_email("Admin", username, signup_email)
                return HttpResponseRedirect('/?active=false')
        else:
            request.session['error_message'] = "Sorry. Something unexpected happened, please try again. (request)"
            return HttpResponseRedirect('/error?signup=fail')
    except:  # if logging in fails, let's try signing them up
        request.session['error_message'] = "Sorry. Something unexpected happened, please try again. (exception)"
        return HttpResponseRedirect('/error?signup=fail')


def error(request):
    return render(request, 'home/error.html')


def send_email(type=None, username=None, email=None):
    """
    Send email to admin or user.
    :param email:
    :return:
    """
    
    try:
        if type == "User":
            print('user email')
            msg = EmailMultiAlternatives(
                subject="Account Pending Notification",
                body="Your account is pending approval, please wait for admin approval.",
                from_email="no_reply@teamedup.com.au",
                to=[username + "<" + email + ">"])
            
            # Optional Anymail extensions:
            msg.tags = ["Pending"]
        
        else:
            print('admin email')
            msg = EmailMultiAlternatives(
                subject="Waiting for approval",
                body="a new user has signed up and their account is pending approval.\n"
                     " Account email is " + email + "\n"
                     " User Name is " + username,
                from_email="no_reply@teamedup.com.au",
                to=["Admin<youdontseemehaha@gmail.com>"])
            
            msg.tags = ["Approving"]
        
        msg.send()
    except Exception as e:
        print('Exception: {}'.format(e))
