from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^new/$', views.new, name='newEvents'),
    url(r'^feature/$', views.feature, name='featureEvents'),
    url(r'^search/$', views.search, name='searchEvents'),
    url(r'^update/$', views.update, name='updateEvents'),
    url(r'^notification/$', views.notification, name='notifyEvents'),

    # ex: /polls/5/
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<event_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^(?P<event_id>[0-9]+)/delete$', views.delete, name='delete'),
]
