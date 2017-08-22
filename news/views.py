# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import News, Category
import datetime

from django.contrib.auth.models import User


# Create your views here.
@login_required
def index(request):
    news_list = News.objects.all().order_by('-pub_date').exclude(is_page=True)
    total_articles = news_list.count()

    navbar_pages = News.objects.filter(display_in_navbar=True)

    # Return three articles to render in the featured articles fields in template
    featured_news_list = News.objects.filter(featured=True).exclude(is_page=True).order_by('-pub_date')[1:3]
    primary_feature = News.objects.order_by('feature_rank').exclude(is_page=True).order_by('-pub_date')[0]
    category_list = Category.objects.all()

    try:
        feature_list = News.objects.order_by('-pub_date').exclude(is_page=True).order_by('-feature_rank')[0:3]

    except:
        feature_list = False

    # pagination of news results
    # paginator = Paginator(news_list, 5)  # show X results per page
    # page = request.GET.get('page')
    # try:
    #     latest_news_list = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     latest_news_list = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     latest_news_list = paginator.page(paginator.num_pages)

    context = {
        # 'latest_news_list': latest_news_list,
        'latest_news_list': news_list,
        'primary_feature': primary_feature,
        'featured_news_list': featured_news_list,
        'feature_list': feature_list,
        'total_articles': total_articles,
        'category_list': category_list,
        'navbar_pages': navbar_pages,
    }
    return render(request, 'news/news.html', context)


@login_required
def detail(request, news_article_id):
    # return HttpResponse('Hello from Python!')

    # return latest four articles to present as 'related news'. Change to be related to tags in future (so that it is genuinely related news)

    news_article = News.objects.get(id=news_article_id)
    related_news = News.objects.filter().exclude(is_page=True).order_by('-pub_date')[0:4]
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

    return render(request, 'news/news-details.html', context)

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

        news_article = News(title=title, article=body, feature_rank=feature_rank, pub_date=pub_date, owner=owner, is_page=is_page, display_in_navbar=display_in_navbar)
        news_article.save()
        
        news_article.category.add(tag)
        
        return redirect('/dashboard')

    return render(request, 'news/news-edit.html', context)


@login_required
def edit(request, news_article_id):
    # return HttpResponse('Hello from Python!')
    # return latest four articles to present as 'related news'. Change to be related to tags in future (so that it is genuinely related news)

    news_article = News.objects.get(id=news_article_id)
    related_news = News.objects.filter().order_by('-pub_date')[0:4]
    try:
        next_url = request.GET['next']
    except:
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
        body = request.POST['body']
        title = request.POST['title']

        feature_rank = request.POST.get('feature_rank', None)
        selected_tag = request.POST.get('category', None)

        is_page = request.POST.get('is_page', None)
        if is_page == 'OK':
            is_page = True
        else:
            is_page=False

        display_in_navbar = request.POST.get('display_in_navbar', None)
        if display_in_navbar == 'OK':
            display_in_navbar = True
        else:
            display_in_navbar=False

        tag = Category.objects.filter(tag=selected_tag).first()

        news_article.article = body
        news_article.title = title
        news_article.feature_rank = feature_rank
        news_article.category.add(tag)
        news_article.is_page = is_page
        news_article.display_in_navbar = display_in_navbar

        news_article.save()

        return redirect('detail', news_article_id=news_article.id)

    return render(request, 'news/news-edit.html', context)


@login_required
def delete(request, news_article_id):
    
    news_article = News.objects.get(id=news_article_id)
    news_article.delete()
    
    context = {}

    return redirect('/dashboard')

