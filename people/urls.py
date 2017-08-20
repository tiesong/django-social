from django.conf.urls import url

from people import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^create$', views.create, name='create'),
    # ex: /polls/5/
    url(r'^(?P<profile_id>[0-9]+)$', views.profile, name='profile'),
]