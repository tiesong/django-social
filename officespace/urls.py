from django.conf.urls import url

from officespace import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]