from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index),
=======


    url(r'^$', views.index),

    url(r'^list(\d+)/$', views.list),
    url(r'^list(\d+)/(\d+)', views.list),
    url(r"^reset/$", views.reset),

    url(r"^list(\d+)/detail(\d+).html$", views.detail),

>>>>>>> frank123123
]
