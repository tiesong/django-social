from django.conf.urls import url

from dashboard import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/create/$', views.user_create, name='user_create'),
   	url(r'^users$', views.users, name='users'),
    url(r'^users/invitation$', views.user_invitation, name='user_invitation'),
   	url(r'^perks$', views.perks, name='perks'),
   	url(r'^events$', views.events, name='events'),
    url(r'^rooms$', views.rooms, name='rooms'),
    url(r'^rooms/(?P<pk>[0-9]+)/delete/$', views.room_delete, name='room_del'),
    url(r'^rooms/(?P<pk>[0-9]+)/edit/$', views.room_edit, name='room_edit'),
    url(r'^rooms/create/$', views.room_create, name='room_create'),
]
