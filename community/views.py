# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime, json
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from news.models import News
from .models import Profile, Tag, Company
from django.db.models import Q


# Create your views here.
@login_required
def index(request):
    return HttpResponse("Hello world")


@login_required
def people_list(request):
    navbar_pages = News.objects.filter(display_in_navbar=True)
    profile_list = Profile.objects.all().order_by('-advisor')
    tag_list = Tag.objects.all()
    
    per = Paginator(profile_list, 5)
    first_page = per.page(1)
    
    context = {
        'profile_list': first_page,
        'navbar_pages': navbar_pages,
        'tag_list': tag_list,
    }
    return render(request, 'community/people_list.html', context)


@login_required
def update(request):
    page_number = request.GET.get('pg_num', 0)
    
    profile_list = Profile.objects.all().order_by('-advisor')
    per = Paginator(profile_list, 5)
    try:
        per_page = per.page(int(page_number))
        print('per page;{}'.format(per_page))
    
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'profile_list': False,
        }
        return render(request, 'community/people_list_content.html', context)
    
    context = {
        'profile_list': per_page,
    }
    return render(request, 'community/people_list_content.html', context)


@login_required
def category(request):
    tag_name = request.GET.get('category')
    page_number = request.GET.get('pg_num', 0)
    tag_name = str(tag_name).replace("-", " ")
    profile_list = Profile.objects.filter(tags__tag=tag_name).order_by('-advisor')
    
    per = Paginator(profile_list, 5)
    
    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'useprofile_listr_list': False,
        }
        return render(request, 'community/people_list_content.html', context)
    
    context = {
        'profile_list': per_page,
    }
    return render(request, 'community/people_list_content.html', context)


@login_required
def search(request):
    keyword = request.GET.get('keyword', "")
    page_number = request.GET.get('pg_num', 0)
    keyword = str(keyword).replace("-", " ")
    profile_list = Profile.objects.filter(Q(tags__tag__icontains=keyword) | Q(companies__name__icontains=keyword) | Q(
        user__username__icontains=keyword) | Q(user__email__icontains=keyword) | Q(
        user__first_name__icontains=keyword) | Q(user__last_name__icontains=keyword)).order_by('-advisor').distinct()
    
    per = Paginator(profile_list, 5)
    
    try:
        per_page = per.page(int(page_number))
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'profile_list': False,
        }
        return render(request, 'community/people_list_content.html', context)
    
    context = {
        'profile_list': per_page,
    }
    return render(request, 'community/people_list_content.html', context)


@login_required
def tags(request):
    if request.GET.get('profile_id'):
        profile = Profile.objects.get(pk=request.GET['profile_id'])
        tag_list = profile.tags.all()
    else:
        tag_list = Tag.objects.all()
    response = []
    for tag in tag_list:
        response.append({'tag_id': tag.id, 'tag_name': tag.tag})
    
    return HttpResponse(json.dumps(response))


@login_required
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


@login_required
def edit_profile(request, profile_id):
    if (request.user.id != int(profile_id)) and not request.user.is_superuser:
        return redirect(reverse('people_list'))
    
    user = User.objects.get(pk=profile_id)
    navbar_pages = News.objects.filter(display_in_navbar=True)
    tag_list = Tag.objects.all()
    tags = ', '.join(map(lambda x: x.tag, tag_list))
    
    if request.POST:
        try:
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
            User.objects.filter(pk=profile_id).update(first_name=first_name, last_name=last_name, email=email, )
            
            profile = Profile.objects.get(pk=profile_id)
            profile.tags.clear()
            if tags[0] != '':
                for tag in tags:
                    profile.tags.add(tag)
                    profile.save()
            
            Profile.objects.filter(pk=profile_id).update(tagline=tagline, phone_number=phone, website=website,
                                                         twitter=twitter, facebook=facebook, linkedin=linkedin,
                                                         bio=description, )
            
            if request.FILES:
                avatar = request.FILES['avatar']
                profile = Profile.objects.get(pk=profile_id)
                profile.image = avatar
                profile.save()
            
            return redirect(reverse('profile', args=[profile_id]))
        except Exception as e:
            raise e
    
    context = {
        'user': user,
        'navbar_pages': navbar_pages,
        'tags': tags,
    }
    return render(request, 'community/profile-edit.html', context)


def companies(request):
    navbar_pages = News.objects.filter(display_in_navbar=True)
    company_list = Company.objects.all().order_by('-partner')
    # industry_list = Category.objects.all()
    
    per = Paginator(company_list, 5)
    first_page = per.page(1)
    print('first_page: {}'.format(first_page))
    context = {
        'company_list': first_page,
        'navbar_pages': navbar_pages,
        # 'industry_list': industry_list,
    }
    return render(request, 'community/company_list.html', context)


def company(request, company_id):
    navbar_pages = News.objects.filter(display_in_navbar=True)
    company_detail = Company.objects.get(pk=company_id)
    context = {
        'navbar_pages': navbar_pages,
        'company': company_detail
    }
    return render(request, 'community/company.html', context)


@login_required
def update_company(request):
    page_number = request.GET.get('pg_num', 0)
    
    company_list = Company.objects.all().order_by('-partner')
    per = Paginator(company_list, 5)
    try:
        per_page = per.page(int(page_number))
        print('per page;{}'.format(per_page))
    
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'company_list': False,
        }
        return render(request, 'community/company_list_content.html', context)
    
    context = {
        'company_list': per_page,
    }
    return render(request, 'community/company_list_content.html', context)


@login_required
def category_company(request):
    tag_name = request.GET.get('category', None)
    page_number = request.GET.get('pg_num', 0)
    tag_name = str(tag_name).replace("-", " ")
    profile_list = Company.objects.filter(categories__tag=tag_name).order_by('-partner')
    
    per = Paginator(profile_list, 5)
    
    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'company_list': False,
        }
        return render(request, 'community/company_list_content.html', context)
    
    context = {
        'company_list': per_page,
    }
    return render(request, 'community/company_list_content.html', context)


@login_required
def search_company(request):
    keyword = request.GET.get('keyword', "")
    page_number = request.GET.get('pg_num', 0)
    keyword = str(keyword).replace("-", " ")
    company_list = Company.objects.filter(Q(categories__tag__icontains=keyword) | Q(title__icontains=keyword)).order_by('-partner').distinct()
    
    per = Paginator(company_list, 5)
    
    try:
        per_page = per.page(int(page_number))
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'company_list': False,
        }
        return render(request, 'community/company_list_content.html', context)
    
    context = {
        'company_list': per_page,
    }
    return render(request, 'community/company_list_content.html', context)


@login_required
def tags_company(request):
    if request.GET.get('profile_id'):
        profile = Profile.objects.get(pk=request.GET['profile_id'])
        tag_list = profile.tags.all()
    else:
        tag_list = Tag.objects.all()
    response = []
    for tag in tag_list:
        response.append({'tag_id': tag.id, 'tag_name': tag.tag})
    
    return HttpResponse(json.dumps(response))
