from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    # ex: /polls/5/
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
]