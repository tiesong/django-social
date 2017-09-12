# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from news.models import News
from .models import Profile, Tag
from django.db.models import Q

# Create your views here.
def index(request):
	return HttpResponse("Hello world")

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
	profile_list = Profile.objects.filter(Q(tags__tag__icontains=keyword) | Q(companies__name__icontains=keyword) | Q(user__username__icontains=keyword) | Q(user__email__icontains=keyword) | Q(user__first_name__icontains=keyword) | Q(user__last_name__icontains=keyword)).order_by('-advisor').distinct()

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
	if (request.user.id != int(profile_id)) and not request.user.is_superuser:
		return redirect(reverse('people_list'))

	user = User.objects.get(pk=profile_id)
	navbar_pages = News.objects.filter(display_in_navbar=True)
	tag_list = Tag.objects.all()

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
			tags = request.POST.getlist('tags')

			User.objects.filter(pk=profile_id).update(first_name=first_name, last_name=last_name, email=email,)
			profile = Profile.objects.get(pk=profile_id)
			profile.tags.clear()
			for tag in tags:
				profile.tags.add(tag)
				profile.save()
			if request.FILES:
				avatar = request.FILES['avatar']
				upload_date = datetime.datetime.now().strftime('%Y/%m/%d/')
				image_location = settings.MEDIA_ROOT + '/profile_images/' + upload_date
				fs = FileSystemStorage(image_location)
				filename = fs.save(avatar.name, avatar)
				url = 'profile_images/' + upload_date + filename
				Profile.objects.filter(pk=profile_id).update(tagline=tagline, image=url, phone_number=phone, website=website, twitter=twitter, facebook=facebook, linkedin=linkedin, bio=description,)
			else:
				Profile.objects.filter(pk=profile_id).update(tagline=tagline, phone_number=phone, website=website, twitter=twitter, facebook=facebook, linkedin=linkedin, bio=description,)

			return redirect(reverse('profile', args=[profile_id]))
		except Exception as e:
			raise e
	context = {
		'user': user,
		'navbar_pages': navbar_pages,
		'tag_list': tag_list,
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
