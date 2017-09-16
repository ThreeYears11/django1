from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url('^place_order/$', index),
    url('^submit/$', submit),
    url('^order/$', order),
]
