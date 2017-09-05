from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^new/$', views.new, name='new'),
    url(r'^feature/$', views.feature, name='feature'),
    url(r'^search/$', views.search, name='search'),
    url(r'^update/$', views.update, name='update'),

    # ex: /polls/5/
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<event_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^(?P<event_id>[0-9]+)/delete$', views.delete, name='delete'),
]
