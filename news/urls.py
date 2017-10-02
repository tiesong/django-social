from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='updateNews'),
    url(r'^category/$', views.category, name='categoryNews'),
    url(r'^search/$', views.search, name='searchNews'),
    
    url(r'^(?P<news_article_url>.+)/$', views.detail, name='detail'),
    url(r'^(?P<news_article_url>.+)/edit$', views.edit, name='edit'),
    url(r'^(?P<news_article_url>.+)/delete$', views.delete, name='delete'),

]