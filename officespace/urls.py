from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.BookingList.as_view()), name='booking_list'),
	url(r'^create$', login_required(views.create), name='booking_create'),
	url(r'^(?P<pk>[0-9]+)/$', login_required(views.BookingDetail.as_view()), name='booking_detail'),
	url(r'^(?P<pk>[0-9]+)/edit/$', login_required(views.BookingUpdate.as_view()), name='booking_edit'),
	url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.BookingDelete.as_view()), name='booking_del'),
]
