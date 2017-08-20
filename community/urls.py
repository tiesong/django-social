from django.conf.urls import url

from community import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^create$', views.create, name='create'),
    # ex: /polls/5/
    url(r'^people/$', views.people_list, name='people_list'),
    url(r'^people/(?P<profile_id>[0-9]+)$', views.profile, name='profile'),

	url(r'^companies/$', views.companies, name='companies'),
    url(r'^companies/(?P<company_id>[0-9]+)$', views.company, name='company'),
]