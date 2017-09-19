from django.conf.urls import include, url
from django.contrib import admin

from tt_goods import views
urlpatterns = [


    url(r'^$', views.index),
    # url(r'^list(\d+)/$', views.list),
    url(r'^list(\d+)/(\d+)_(\d+)/$', views.list),
    url(r"^detail(\d+)/(\d+)$", views.detail),
    # url(r'^listx(\d+)/', views.listx),
    # url(r'^listx_ajax/', views.listx_ajax),
    url(r"^reset/$", views.reset),


]

