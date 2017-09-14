#! /usr/bin/env python3
# -*-coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register1/$', views.register1),
    url(r'^login/$', views.login),
    url(r'^verify_code/$', views.verify_code),
    url(r'^check_user/$', views.check_user),
    url(r'^check_email/$', views.check_email),
    url(r'^check_login/$', views.check_login),
    url(r'^denglu/$', views.denglu),
    url(r'^active(\d+)/$', views.active),
    url(r'^user_cookie/$', views.login_cookie),
    url(r'^site/$', views.site),
    url(r'^show/$', views.show),
    # url(r'^site_list/$', views.site_list),

]
