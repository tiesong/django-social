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
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^list_company/$', views.list_company, name='list_company'),
    url(r'^people/(?P<profile_id>[0-9]+)$', views.profile, name='profile'),
    url(r'^people/(?P<profile_id>[0-9]+)/edit$', views.edit_profile, name='edit_profile'),
    
    url(r'^update_company/$', views.update_company, name='update_company'),
    url(r'^category_company/$', views.category_company, name='category_company'),
    url(r'^search_company/$', views.search_company, name='searchCompany'),
    url(r'^tags_company/$', views.tags_company, name='tags_company'),
    url(r'^companies/$', views.companies, name='companies'),
    url(r'^companies/(?P<company_id>[0-9]+)$', views.company, name='company'),
    url(r'^companies/(?P<company_id>[0-9]+)/edit$', views.edit_company, name='edit_company'),
]
