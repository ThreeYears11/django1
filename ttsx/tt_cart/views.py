from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from tt_goods.models import *
from tt_cart.models import *
from tt_user .models import *
from django.db.models import Q
from tt_user.user_decorators import *
# Create your views here.
@is_login
def good_data(request):
    #从detail页面获得数据 构造对象
    goods_id = request.GET.get('goods_id')
    goods_num = request.GET.get('goods_num')
    userid = request.session.get('uid')
    good = GoodsInfo.objects.get(id=goods_id)
    cart_list = CartInfo.objects.filter(user_id=userid)
    #如果商品存在 修改数量不构造对象
    for cart in cart_list:
        if cart.goods_id == int(goods_id):
            cart.count += int(goods_num)
            cart.save()
            return JsonResponse({'cid':cart.id})

    cart = CartInfo()
    cart.user_id = userid
    cart.goods = good
    cart.count = int(goods_num)
    cart.save()
    return JsonResponse({'cid':cart.id})
@is_login
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

def count(request):
    c = CartInfo.objects.filter(user_id=request.session.get('uid')).count()
    return JsonResponse({'count':c})