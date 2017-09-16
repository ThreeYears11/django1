#! /usr/bin/env python3
# -*-coding: utf-8 -*-
from django.shortcuts import redirect

def is_login(func):
    def fun(request,*args,**kwargs):
        if request.session.get('uid'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/user/login/')
    return fun
    