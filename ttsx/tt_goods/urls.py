from django.conf.urls import include, url
from django.contrib import admin

from tt_goods import views

urlpatterns = [


    url(r'^$', views.index),

    url(r'^list(\d+)/$', views.list),
    url(r'^list(\d+)/(\d+)', views.list),
    url(r"^reset/$", views.reset),

    url(r"^list(\d+)/detail(\d+).html$", views.detail),

]
