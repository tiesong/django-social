from django.conf.urls import url

from community import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^create$', views.create, name='create'),
    # ex: /polls/5/
    url(r'^people/$', views.people_list, name='people_list'),
    url(r'^update/$', views.update, name='updateUsers'),
    url(r'^category/$', views.category, name='category'),
    url(r'^search/$', views.search, name='searchUsers'),
    url(r'^people/(?P<profile_id>[0-9]+)$', views.profile, name='profile'),
    url(r'^people/(?P<profile_id>[0-9]+)/edit$', views.edit_profile, name='edit_profile'),

	url(r'^companies/$', views.companies, name='companies'),
    url(r'^companies/(?P<company_id>[0-9]+)$', views.company, name='company'),
]
