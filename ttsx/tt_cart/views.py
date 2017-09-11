from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *


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



