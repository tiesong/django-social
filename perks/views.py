# Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Perks, Category
from bs4 import BeautifulSoup
import datetime

from news.models import News

from django.contrib.auth.models import User


# Create your views here.
@login_required
def index(request):

    news_list = Perks.objects.all().order_by('-pub_date').exclude(is_page=True)
    total_articles = news_list.count()
    

    per = Paginator(news_list, 5)
    # total_page = per.count()
    first_page = per.page(1)
    navbar_pages = News.objects.filter(display_in_navbar=True)

    # Return three articles to render in the featured articles fields in template
    featured_news_list = Perks.objects.filter(featured=True).exclude(is_page=True).order_by('-pub_date')[1:3]
    primary_feature = Perks.objects.order_by('feature_rank').exclude(is_page=True).order_by('-pub_date')[0]
    category_list = Category.objects.all()

    try:
        feature_list = Perks.objects.order_by('-pub_date').exclude(is_page=True).order_by('-feature_rank')[0:3]

    except:
        feature_list = False

    context = {
        'news_list': first_page,
        'primary_feature': primary_feature,
        'featured_news_list': featured_news_list,
        'feature_list': feature_list,
        'total_articles': total_articles,
        'category_list': category_list,
        'navbar_pages': navbar_pages,
    }
    return render(request, 'perks/news.html', context)


@login_required
def update(request):
    page_number = request.GET.get('pg_num', 0)

    news_list = Perks.objects.all().order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)

    try:
        per_page = per.page(int(page_number))
        print('per page;{}'.format(per_page))

    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'perks/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'perks/news-content.html', context)


@login_required
def category(request):
    print('category')
    category_name = request.GET.get('category')
    page_number = request.GET.get('pg_num', 0)
    category_name = str(category_name).replace("-", " ")
    tag = Category.objects.filter(tag=category_name).first()
    news_list = Perks.objects.filter(category=tag).order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'perks/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'perks/news-content.html', context)


@login_required
def search(request):
    """
    
    :param request: 
    :return: 
    """

    keyword = request.GET.get('keyword', "")
    page_number = request.GET.get('pg_num', 0)
    keyword = str(keyword).replace("-", " ")

    if keyword == "":
        context = {
            'news_list': False,
        }
        return render(request, 'perks/news-content.html', context)

    news_list = Perks.objects.filter(title__icontains=keyword).order_by('-pub_date').exclude(is_page=True)

    if len(news_list) == 0:
        news_list = Perks.objects.filter(article__icontains=keyword).order_by('-pub_date').exclude(is_page=True)

    per = Paginator(news_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'perks/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'perks/news-content.html', context)


@login_required
def detail(request, news_article_id):

    news_article = Perks.objects.get(id=news_article_id)
    related_news = Perks.objects.filter().exclude(is_page=True).order_by('-pub_date')[0:4]
    navbar_pages = News.objects.filter(display_in_navbar=True)

    try:
        next_url = request.GET['next']
    except:
        next_url = False

    context = {
        'navbar_pages': navbar_pages,
        'news_article': news_article,
        'related_news': related_news,
        'next': next_url,
    }

    return render(request, 'perks/news-details.html', context)


@login_required
def create(request):
    try:
        next_url = request.GET['next']

    except:
        next_url = False

    categories = Category.objects.all()
    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'categories': categories,
        'create': True,
        'next': next_url,
        'navbar_pages': navbar_pages
    }

    if request.POST:
        owner = request.user

        body = request.POST['body']
        title = request.POST['title']

        feature_rank = request.POST.get('feature_rank', None)
        pub_date = datetime.datetime.now()
        selected_tag = request.POST.get('category', None)

        tag = Category.objects.filter(tag=selected_tag).first()

        is_page = request.POST.get('is_page', None)
        if is_page == 'OK':
            is_page = True
        else:
            is_page = False

        display_in_navbar = request.POST.get('display_in_navbar', None)
        if display_in_navbar == 'OK':
            display_in_navbar = True
        else:
            display_in_navbar = False

        news_article = Perks(title=title, article=body, feature_rank=feature_rank, pub_date=pub_date, owner=owner,
                            is_page=is_page, display_in_navbar=display_in_navbar)
        news_article.save()

        news_article.category.add(tag)

        return redirect('/dashboard/perks')

    return render(request, 'perks/news-edit.html', context)


@login_required
def edit(request, news_article_id):

    news_article = Perks.objects.get(id=news_article_id)
    related_news = Perks.objects.filter().order_by('-pub_date')[0:4]
    try:
        next_url = request.GET['next']
    except:
        next_url = False

    categories = Category.objects.all()
    navbar_pages = Perks.objects.filter(display_in_navbar=True)

    context = {
        'categories': categories,
        'news_article': news_article,
        'related_news': related_news,
        'next': next_url,
        'navbar_pages': navbar_pages,
    }

    if request.POST:
        try:
            body = request.POST['body']
            title = request.POST['title']

            feature_rank = request.POST.get('feature_rank', None)
            selected_tag = request.POST.get('category', None)

            is_page = request.POST.get('is_page', None)
            if is_page == 'OK':
                is_page = True
            else:
                is_page = False

            display_in_navbar = request.POST.get('display_in_navbar', None)
            if display_in_navbar == 'OK':
                display_in_navbar = True
            else:
                display_in_navbar = False

            tag = Category.objects.filter(tag=selected_tag).first()

            news_article.article = body
            news_article.title = title
            news_article.feature_rank = feature_rank
            news_article.category.add(tag)
            news_article.is_page = is_page
            news_article.display_in_navbar = display_in_navbar

            news_article.save()

            return redirect('detail', news_article_id=news_article.id)
        except Exception as e:
            print ('Error: {}'.format(e))
    return render(request, 'perks/news-edit.html', context)


@login_required
def delete(request, news_article_id):
    news_article = Perks.objects.get(id=news_article_id)
    news_article.delete()

    context = {}

    return redirect('/dashboard')
