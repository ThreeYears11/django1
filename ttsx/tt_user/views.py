from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

# Create your views here.
def islogin(request):
    islogin = request.session.get('isLogin')
    uname = request.session.get('uname')
    print(islogin)
    return JsonResponse({'islogin': islogin, 'uname': uname})