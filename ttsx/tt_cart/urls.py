from django.conf.urls import url
from . import views
urlpatterns = [

    # url(r'^detail/$',views.detail),
    url(r'^good_data/$',views.good_data),
    url(r'^center/$',views.center),
    url(r'^change_data1/$',views.change_data1),
    url(r'^change_data2/$',views.change_data2),
    url(r'^delete_data/$',views.delete_data),
]