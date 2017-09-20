#! /usr/bin/env python3
# -*-coding: utf-8 -*-
"""
   url(r'^verify_code/$',views.verify_code),
    url(r'^yzm/$',views.yzm),
    url(r'^yzm2/$',views.yzm2),
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
    url(r'^show/$',views.show),
    url(r'^add_addr/$',views.add_addr),
    url(r'^current/$',views.current),
    url(r'^site_cur/$',views.site_cur),
    url(r'^xiugai/$', views.xiugai),
    url(r'^info/$',views.info),
    url(r'^order/$',views.order),
    url(r'^logout/$',views.logout),
    url(r'^check_yzm/$',views.check_yzm),

"""
class GetPathMiddleware():
    def process_view(self,request,vies_func,vies_args,vies_kwargs):
        no_path = [
            '/user/register/',
            '/user/register1/',
            '/user/login/',
            '/user/denglu/',
            '/user/check_user/',
            '/user/check_email/',
            '/user/check_login/',
            '/user/yzm/',
            '/user/verify_code/',
            '/user/check_yzm/',
            '/user/yzm/',
            '/user/yzm2/',
            '/user/user_cookie/',
            '/user/check_yzm/',
            '/user/xiugai/',
            '/user/add_addr/',
            '/user/current/',
            '/user/site_cur/',
            '/cart/good_data/',
            '/cart/count/',

        ]
        if request.path not in no_path and 'active' not in request.path:
            request.session['url_path'] = request.get_full_path()


    