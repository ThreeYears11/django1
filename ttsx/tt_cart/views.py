from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from tt_goods.models import *
from tt_cart.models import *
from tt_user .models import *
from django.db.models import Q

# Create your views here.

def detail(request):
    return render(request,'tt_cart/detail.html')
def good_data(request):
    #从detail页面获得数据 构造对象
    good_id = request.GET.get('good_id')
    user_id = request.GET.get('user_id')
    good = GoodsInfo.objects.get(id=good_id)
    user = UserInfo.objects.get(id=user_id)
    cart_list = CartInfo.objects.filter(user_id=user_id)
    #如果商品存在 修改数量不构造对象
    for cart in cart_list:
        if cart.goods_id == int(good_id):
            cart.count += 1
            cart.save()
            return

    cart = CartInfo()
    cart.user = user
    cart.goods = good
    cart.count = 1
    cart.save()
    return HttpResponse('ok')
def center(request):
    cart_list = CartInfo.objects.filter(user_id=1)
    context = {'cart_list':cart_list}
    return render(request,'tt_cart/cart.html',context)
#加号修改数据
def change_data1(request):
    good_id = request.GET.get('good_id')
    user_id = request.GET.get('user_id')
    count = int(request.GET.get('count'))
    cart_li = CartInfo.objects.filter(goods_id=good_id).filter(user_id=user_id)
    for cart in cart_li:
        cart.count = count+1
        cart.save()
    return HttpResponse('ok')
#减号修改数据
def change_data2(request):
    good_id = request.GET.get('good_id')
    user_id = request.GET.get('user_id')
    count = int(request.GET.get('count'))
    cart_li = CartInfo.objects.filter(goods_id=good_id).filter(user_id=user_id)
    for cart in cart_li:
        if count == 0:
            count = 1
        cart.count = count-1
        cart.save()
    return HttpResponse('ok')
#删除数据
def delete_data(request):
    good_id = request.GET.get('good_id')
    user_id = request.GET.get('user_id')
    cart_li = CartInfo.objects.filter(goods_id=good_id).filter(user_id=user_id)
    for cart in cart_li:
        cart.delete()
    return HttpResponse('ok')