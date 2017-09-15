from django.core.files.storage import FileSystemStorage
<<<<<<< HEAD
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *

=======
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from tt_goods.models import *
from tt_cart.models import *
from tt_user .models import *
from django.db.models import Q
>>>>>>> frank123123

# Create your views here.
def cart(request):
    id = 1
    cart = CartInfo.objects.filter(user_id=id)
    content = {'list': cart}
    return render(request, 'tt_cart/cart.html', content)


def delete(request):
    goods_id = request.POST.get('id')
    print(goods_id)
    cart = CartInfo.objects.get(goods_id=goods_id)
    cart.delete()
    return redirect('/cart/123456/')


def add(request):
    goods_id = request.POST.get('id')
    add = request.POST.get('add')
    print(goods_id, add)
    cart = CartInfo.objects.get(goods_id=goods_id)
    cart.count += int(add)
    cart.save()
    return redirect('/cart/123456/')

def good_data(request):
    #从detail页面获得数据 构造对象
    goods_id = request.GET.get('goods_id')
    goods_num = request.GET.get('goods_num')
    print(goods_id,goods_num)
    # user_id = request.GET.get('user_id')
    good = GoodsInfo.objects.get(id=goods_id)
    user = UserInfo.objects.get(id=1)
    cart_list = CartInfo.objects.filter(user_id=1)
    #如果商品存在 修改数量不构造对象
    for cart in cart_list:
        if cart.goods_id == int(goods_id):
            cart.count += int(goods_num)
            cart.save()
            return JsonResponse({'cid':cart.id})

    cart = CartInfo()
    cart.user = user
    cart.goods = good
    cart.count = 1
    cart.save()
    return JsonResponse({'cid':cart.id})
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