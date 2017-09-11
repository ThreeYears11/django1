from django.conf.urls import url
from . import views

urlpatterns = [
    url('^123456/$', views.cart),
    url('^delete/$', views.delete),
    url('^add/$', views.add),
]
