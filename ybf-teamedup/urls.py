from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.views import defaults
from django.contrib import admin
import notifications.urls
admin.autodiscover()

import home.views, news.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #password reset URLS
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^$', home.views.index, name='index'),
    url(r'^error/', home.views.error, name='error'),
    url(r'^404/$', defaults.page_not_found),
    url(r'^500/$', defaults.server_error),
    url(r'^signup/', home.views.signup, name='signup'),
	url(r'^tinymce/', include('tinymce.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^perks/', include('perks.urls')),
    url(r'^c/', include('community.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^office/', include('officespace.urls')),
	url(r'^events/', include('events.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^officespace/', include('officespace.urls')),
    url('^', include('django.contrib.auth.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
