from django.conf.urls import url
import views
urlpatterns=[
	url(r'^register/$',views.register),
	url(r'^register_handle/$',views.register_handle),
	url(r'^register_exist/$',views.register_exist),
	url(r'^login/$',views.login),
	url(r'^login_handle/$',views.login_handle),
	url(r'^info/$',views.info),
	url(r'^site/$',views.site),
	url(r'^site_handle/$',views.site_handle),
]