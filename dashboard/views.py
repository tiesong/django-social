# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
import math

from news.models import News
from perks.models import Perks
from events.models import Event
from officespace.models import Room
from community.models import Profile, Tag, Company
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.hashers import make_password


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    news_list = News.objects.all().order_by('-pub_date')
    total_articles = news_list.count()
    per = Paginator(news_list, 15)

    pg_num = request.GET.get('pg_num', None)
    
    if (total_articles/15) > int(total_articles/15):
        total_pages = int(total_articles/15) + 1
    else:
        total_pages = int(total_articles/15)

    pg_num = int(pg_num) if pg_num else 1
    print('pg_num: {}'.format(pg_num))
    
    try:
        first_page = per.page(pg_num)
    except Exception as e:
        print('Error: {}'.format(e))
        first_page = per.page(pg_num)
    
    context = {
        'news_list': first_page,
        'total_pages': range(total_pages),
        'total_count': total_articles,
        'pg_num': pg_num
    }
    return render(request, 'dashboard/content_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update(request):
    page_number = request.GET.get('pg_num', 0)

    news_list = News.objects.all().order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)

    try:
        per_page = per.page(int(page_number))
        print('per page;{}'.format(per_page))

    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'news/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'news/news-content.html', context)


@user_passes_test(lambda u: u.is_superuser)
def perks(request):
    news_list = Perks.objects.all().order_by('-pub_date')
    total_articles = news_list.count()
    per = Paginator(news_list, 15)

    pg_num = request.GET.get('pg_num', None)

    if (total_articles / 15) > int(total_articles / 15):
        total_pages = int(total_articles / 15) + 1
    else:
        total_pages = int(total_articles / 15)

    pg_num = int(pg_num) if pg_num else 1
    print('pg_num: {}'.format(pg_num))
    try:
        first_page = per.page(pg_num)
    except Exception as e:
        print('Error: {}'.format(e))
        first_page = per.page(pg_num)

    context = {
        'news_list': first_page,
        'total_pages': range(total_pages),
        'total_count': total_articles,
        'pg_num': pg_num
    }
    
    return render(request, 'dashboard/perks_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    user_list = Profile.objects.all().order_by('user__username')
    total_articles = user_list.count()
    per = Paginator(user_list, 15)

    pg_num = request.GET.get('pg_num', None)

    if (total_articles / 15) > int(total_articles / 15):
        total_pages = int(total_articles / 15) + 1
    else:
        total_pages = int(total_articles / 15)

    print('total_pages: {}'.format(total_pages))
    pg_num = int(pg_num) if pg_num else 1
    print('pg_num: {}'.format(pg_num))

    try:
        first_page = per.page(pg_num)
    except Exception as e:
        print('Error: {}'.format(e))
        first_page = per.page(pg_num)

    context = {
        'user_list': first_page,
        'total_pages': range(total_pages),
        'total_count': total_articles,
        'pg_num': pg_num
    }
    print('user context: {}'.format(context))
    return render(request, 'dashboard/users_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    tag_list = Tag.objects.all()
    all_tags = ', '.join(map(lambda x: x.tag, tag_list))
    context = {'all_tags': all_tags, }
    
    if request.POST:
        name = request.POST['name']
        if name:
            first_name = name.split(' ')[0]
            if len(name.split(' ')) > 1:
                last_name = name.split(' ')[1]
            else:
                last_name = ''
        else:
            first_name = ''
            last_name = ''
        
        tagline = request.POST['tagline']
        email = request.POST['email']
        phone = request.POST['phone']
        
        website = request.POST['website']
        twitter = request.POST['twitter']
        facebook = request.POST['facebook']
        linkedin = request.POST['linkedin']
        description = request.POST['description']
        tags = request.POST['tags'].split(',')
        company_tags = request.POST['companies'].split(',')
        
        try:
            exist_status = User.objects.filter(email=email).exists()
            
            if exist_status:
                context = {
                    'all_tags': all_tags,
                    'exist_status': exist_status,
                    'first_name': first_name,
                    'last_name': last_name,
                    'tagline': tagline,
                    'email': email,
                    'phone': phone,
                    'website': website,
                    'twitter': twitter,
                    'facebook': facebook,
                    'linkedin': linkedin,
                    'description': description,
                }
                
                return render(request, 'dashboard/users_create_dashboard.html', context)
            
            password = User.objects.make_random_password(length=8)
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            
            profile = Profile.objects.get(pk=user.id)
            profile.tags.clear()
            if tags[0] != '':
                for tag in tags:
                    profile.tags.add(tag)
                    profile.save()
            
            profile.companies.clear()
            print(company_tags)
            if len(company_tags) != 0:
                for tag in company_tags:
                    
                    if Company.objects.filter(title=tag).exists():
                        profile.companies.add(Company.objects.filter(title=tag).values_list('id', flat=True)[0])
                    else:
                        new_company = Company(title=tag)
                        new_company.save()
                        profile.companies.add(new_company.id)
                    
                    profile.save()
            
            Profile.objects.filter(pk=user.id).update(temp_password=password, tagline=tagline, phone_number=phone,
                                                      website=website, twitter=twitter, facebook=facebook,
                                                      linkedin=linkedin, bio=description)
            
            if request.FILES:
                avatar = request.FILES['avatar']
                profile = Profile.objects.get(pk=user.id)
                profile.image = avatar
                profile.save()
            
            user_list = Profile.objects.all().order_by('user__username')
            context = {
                'user_list': user_list,
            }
            
            return render(request, 'dashboard/users_dashboard.html', context)
        except Exception as e:
            raise e
    
    return render(request, 'dashboard/users_create_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_active(request, pk):
    """
    Set user signed up as active
    :param request:
    :return:
    """
    user = User.objects.filter(pk=pk).get()
    user.is_active = True
    user.save()
    send_email(user.username, user.email)
    return JsonResponse({'result': 'active'})


@user_passes_test(lambda u: u.is_superuser)
def user_inactive(request, pk):
    """
    Set user signed up as inactive
    :param request:
    :return:
    """
    user = User.objects.filter(pk=pk).get()
    user.is_active = False
    user.save()
    return JsonResponse({'result': 'inactive'})


@user_passes_test(lambda u: u.is_superuser)
def news_active(request, pk):
    """
    Set user signed up as active
    :param request:
    :return:
    """
    article = News.objects.filter(pk=pk).get()
    article.public = True
    article.save()
    return JsonResponse({'result': 'active'})


@user_passes_test(lambda u: u.is_superuser)
def news_inactive(request, pk):
    """
    Set user signed up as inactive
    :param request:
    :return:
    """
    article = News.objects.filter(pk=pk).get()
    article.public = False
    article.save()
    return JsonResponse({'result': 'active'})


@user_passes_test(lambda u: u.is_superuser)
def event_active(request, pk):
    """
    Set user signed up as active
    :param request:
    :return:
    """
    article = Event.objects.filter(pk=pk).get()
    article.public = True
    article.save()
    return JsonResponse({'result': 'active'})


@user_passes_test(lambda u: u.is_superuser)
def event_inactive(request, pk):
    """
    Set user signed up as inactive
    :param request:
    :return:
    """
    article = Event.objects.filter(pk=pk).get()
    article.public = False
    article.save()
    return JsonResponse({'result': 'active'})


@user_passes_test(lambda u: u.is_superuser)
def user_invitation(request):
    to_email = request.GET['email']
    to_email = str(to_email).replace(" ", "+")
    user_id = request.GET['user_id']
    username = request.GET['username']
    username = str(username).replace(" ", "+")
    from_email = settings.DEFAULT_FROM_EMAIL
    password = Profile.objects.filter(pk=user_id).values_list('temp_password', flat=True).first()
    subject = 'Invitation to join into York Butter Factory'
    message = 'Hi, \n\n\n' + \
              'This email is to help you join to York Butter Factory.\n\n' + \
              'Temporary account information\n' + \
              'Username: ' + username + \
              '\nPassword: ' + password + \
              '\n\nPlease click the ' + settings.SITE_URL + ' with the temporary information to continue to join us.\n' + \
              'To change the password, please go to ' + settings.SITE_URL + '/password_reset.\n' + \
              'If clicking the links above does not work, please copy and paste the URL in a new browser window instead.\n\n\n' + \
              'Sincerely,\n' + \
              'The team at YBF'
    
    try:
        status = send_mail(subject, message, from_email, [to_email], )
        if status:
            Profile.objects.filter(pk=user_id).update(invitation_status=True)
            return redirect(reverse('users'))
    except Exception as e:
        raise e


@user_passes_test(lambda u: u.is_superuser)
def events(request):
    event_list = Event.objects.all().order_by('-start_date')
    total_articles = event_list.count()
    per = Paginator(event_list, 15)

    pg_num = request.GET.get('pg_num', None)

    if (total_articles / 15) > int(total_articles / 15):
        total_pages = int(total_articles / 15) + 1
    else:
        total_pages = int(total_articles / 15)

    pg_num = int(pg_num) if pg_num else 1
    print('pg_num: {}'.format(pg_num))

    print('pg_num: {}'.format(pg_num))
    try:
        first_page = per.page(pg_num)
    except Exception as e:
        print('Error: {}'.format(e))
        first_page = per.page(pg_num)

    context = {
        'event_list': first_page,
        'total_pages': range(total_pages),
        'total_count': total_articles,
        'pg_num': pg_num
    }
    
    return render(request, 'dashboard/events_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def rooms(request):
    room_list = Room.objects.all().order_by('category')
    total_articles = room_list.count()
    per = Paginator(room_list, 15)

    pg_num = request.GET.get('pg_num', None)

    if (total_articles / 15) > int(total_articles / 15):
        total_pages = int(total_articles / 15) + 1
    else:
        total_pages = int(total_articles / 15)
    
    pg_num = int(pg_num) if pg_num else 1
    print('pg_num: {}'.format(pg_num))
    
    try:
        first_page = per.page(pg_num)
    except Exception as e:
        print('Error: {}'.format(e))
        first_page = per.page(pg_num)

    context = {
        'room_list': first_page,
        'total_pages': range(total_pages),
        'total_count': total_articles,
        'pg_num': pg_num
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


def send_email(username=None, email=None):
    """
    Send email to admin or user.
    :param email:
    :return:
    """
    print('sending mail')
    try:
        msg = EmailMultiAlternatives(
            subject="Your account has already been approved",
            body="Your account has been approved by admin",
            from_email="no_reply@teamedup.com.au",
            to=[username + "<" + email + ">"])
        
        msg.tags = ["Approved"]
        msg.track_clicks = True
    
        msg.send()
    except Exception as e:
        print('Exception: {}'.format(e))