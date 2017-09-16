import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from tt_cart.models import *
from .models import *
from django.db import transaction


# Create your views here.
@transaction.atomic
def index(request):
    car_id_list = request.POST.getlist('cid')
    if not car_id_list:
        car_id_list = request.GET.getlist('cid')
    print(car_id_list)
    # car_id_list = [15, 16]
    total = 0
    flag = True
    flag1 = True
    sid = transaction.savepoint()
    for car_id in car_id_list:
        car_id = str(car_id)
        car = CartInfo.objects.get(id=car_id)
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dt = time.strftime("%Y%m%d%H%M%S", time_local)
        oid = dt + str(car.user_id)
        if flag:
            order = OrderInfo()
            order.oid = oid
            order.user_id = car.user_id
            order.ototal = total
            order.oaddress = 'abcdef'
            order.save()
            flag = False
        od = OrderDetailInfo()
        od.goods_id = car.goods.id
        od.order_id = oid
        od.price = car.goods.gprice
        od.count = car.count
        if od.count > car.goods.gkucun:
            flag1 = False
            break
        # print(od.goods_id, od.order_id, od.price, od.count)
        od.goods.gkucun -= od.count
        od.goods.save()
        od.save()
        car.delete()
        total += od.price * od.count
    if flag1:
        order.ototal = total
        print(order.ototal)
        order.save()
        transaction.savepoint_commit(sid)
    else:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/center/')
    content = {'order': order}
    return render(request, 'tt_order/place_order.html', content)


def submit(request):
    oid = request.POST.get('oid')
    o = OrderInfo.objects.get(oid=oid)
    o.oIsPay = 1
    o.save()
    return HttpResponse('<a href="/">付款成功,点击继续购物</a>')
