from django.conf.urls import url

from dashboard import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
   	url(r'^users$', views.users, name='users'),
   	url(r'^perks$', views.perks, name='perks'),
   	url(r'^events$', views.events, name='events'),
]