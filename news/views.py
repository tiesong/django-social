# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from functools import wraps

from django.urls import reverse
from django.utils.decorators import available_attrs

from .models import News, Category
import datetime


def check_public(view_func):
    def _decorator(request, *args, **kwargs):
        news_article_url = kwargs['news_article_url']

        if not news_article_url:
            return HttpResponseRedirect('/')

        news_article_id = news_article_url.split('-')[0]
        news_article = News.objects.get(id=news_article_id)
        if news_article.public or request.user.is_authenticated():
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponseRedirect('/')

    return wraps(view_func)(_decorator)


# Create your views here.
@login_required
def index(request):
    news_list = News.objects.all().order_by('-pub_date').exclude(is_page=True)
    total_articles = news_list.count()
    
    if (total_articles/5) > round(total_articles/5):
        total_pages = int(total_articles/5) + 1
    else:
        total_pages = int(total_articles/5)
        
    per = Paginator(news_list, 5)
    first_page = per.page(1)
    navbar_pages = News.objects.filter(display_in_navbar=True)
    
    # Return three articles to render in the featured articles fields in template
    featured_news_list = News.objects.filter(featured=True).exclude(is_page=True).order_by('-pub_date')[1:3]
    primary_feature = News.objects.order_by('feature_rank').exclude(is_page=True).order_by('-pub_date')[0]
    category_list = Category.objects.all()
    
    try:
        feature_list = News.objects.order_by('-pub_date').exclude(is_page=True).order_by('-feature_rank')[0:3]
    
    except Exception as e:
        print('Exception: {}'.format(e))
        feature_list = False
    
    context = {
        'news_list': first_page,
        'primary_feature': primary_feature,
        'featured_news_list': featured_news_list,
        'feature_list': feature_list,
        'total_articles': total_articles,
        'total_pages': total_pages,
        'category_list': category_list,
        'navbar_pages': navbar_pages,
    }
    return render(request, 'news/news.html', context)


@login_required
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


@login_required
def category(request):
    print('category')
    category_name = request.GET.get('category')
    page_number = request.GET.get('pg_num', 0)
    category_name = str(category_name).replace("-", " ")
    tag = Category.objects.filter(tag=category_name).first()
    news_list = News.objects.filter(category=tag).order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)
    
    try:
        per_page = per.page(page_number)
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
        return render(request, 'news/news-content.html', context)
    
    news_list = News.objects.filter(Q(title__icontains=keyword) | Q(article__icontains=keyword)) \
        .order_by('-pub_date').exclude(is_page=True).distinct()
    print('news_list: {}'.format(news_list))
    per = Paginator(news_list, 5)
    
    try:
        per_page = per.page(page_number)
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


@check_public
def detail(request, news_article_url):
    if request.user.is_authenticated():
        logged = False
    else:
        logged = True
    news_article_id = news_article_url.split('-')[0]
    news_article = News.objects.get(id=news_article_id)
    related_news = News.objects.filter().exclude(is_page=True).order_by('-pub_date')[0:4]
    navbar_pages = News.objects.filter(display_in_navbar=True)
    
    try:
        next_url = request.GET['next']
    except Exception as e:
        print('detail next url Error: {}'.format(e))
        next_url = False
    
    context = {
        'navbar_pages': navbar_pages,
        'news_article': news_article,
        'related_news': related_news,
        'logged': logged,
        'next': next_url,
    }
    
    return render(request, 'news/news-details.html', context)


@login_required
def create(request):
    try:
        next_url = request.GET['next']
    
    except Exception as e:
        print('create Error: {}'.format(e))
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
        
        news_article = News(title=title, article=body, feature_rank=feature_rank, pub_date=pub_date, owner=owner,
                            is_page=is_page, display_in_navbar=display_in_navbar)
        news_article.save()
        
        news_article.category.add(tag)
        
        return redirect('/dashboard')
    
    return render(request, 'news/news-edit.html', context)


@login_required
def edit(request, news_article_url):
    news_article_id = news_article_url.split('-')[0]
    news_article = News.objects.get(id=news_article_id)
    
    if not request.user.is_superuser:
        if not news_article.owner:
            return redirect('detail', news_article_url=news_article_url)
        elif request.user.id != news_article.owner.id:
            return redirect('detail', news_article_url=news_article_url)
    
    related_news = News.objects.filter().order_by('-pub_date')[0:4]
    try:
        next_url = request.GET['next']
    except Exception as e:
        print('Error: {}'.format(e))
        next_url = False
    
    categories = Category.objects.all()
    navbar_pages = News.objects.filter(display_in_navbar=True)
    
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
            if next_url:
                pub_date = request.POST['pub_date']
            
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
            if next_url:
                news_article.pub_date = pub_date
            
            news_article.save()
            
            if next_url:
                return redirect('/dashboard')
            else:
                url = str(news_article.id) + "-" + news_article.title.replace(" ", "-")
                return redirect('detail', news_article_url=url)
        
        except Exception as e:
            print ('Error: {}'.format(e))
    return render(request, 'news/news-edit.html', context)


@login_required
def delete(request, news_article_url):
    news_article_id = news_article_url.split('-')[0]
    news_article = News.objects.get(id=news_article_id)
    news_article.delete()
    
    return redirect('/dashboard')
