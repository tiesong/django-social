from django.conf.urls import url

from perks import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='updatePerks'),
    url(r'^category/$', views.category, name='categoryPerks'),
    url(r'^search/$', views.search, name='searchPerks'),
    # url(r'^search/(?P<keyword>.+)/$', views.search, name='search'),
    # ex: /polls/5/
    url(r'^(?P<news_article_id>[0-9]+)/$', views.detail, name='perks_detail'),
    url(r'^(?P<news_article_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^(?P<news_article_id>[0-9]+)/delete$', views.delete, name='delete'),

]