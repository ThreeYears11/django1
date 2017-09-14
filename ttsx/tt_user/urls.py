#! /usr/bin/env python3
# -*-coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/^user_center_info_get/$', views.user_center_info_get),
]


    