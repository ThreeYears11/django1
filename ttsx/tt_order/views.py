from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from .models import *
from tt_goods.models import GoodsInfo
from tt_user.models import *
from .models import OrderInfo, OrderDetailInfo
import time


# Create your views here.
def place_order(request):
    id = request.GET.get('id')
    order = OrderInfo.objects.get(oid=id)
    goods = order.orderdetailinfo_set.all()
    phone = order.user.useraddressinfo_set.all()[0]
    content = {'user': order, 'phone': phone, 'goods': goods, 'oid': id}
    return render(request, "tt_order/place_order.html", content)


def order_add(request):
    uid = 1
    gid = request.POST.get('goodsid')
    count = request.POST.get('count')
    addr = UserAddressInfo.objects.get(user_id=uid)
    a = OrderInfo()
    dt = time.time()
    time_local = time.localtime(dt)
    dt = time.strftime("%Y%m%d%H%M%S", time_local)
    a.oid = str(dt) + str(uid)
    a.user = UserInfo.objects.get(id=uid)
    a.ototal = 0
    a.oaddress = addr.uaddress
    a.save()
    gid = gid.split(',')
    gid.remove('')
    for g in gid:
        b = OrderDetailInfo()
        b.goods = GoodsInfo.objects.get(id=g)
        b.order = OrderInfo.objects.get(oid=a.oid)
        b.price = GoodsInfo.objects.get(id=g).gprice
        b.count = count
        b.save()
    return JsonResponse({'oid': a.oid})


def submit(request):
    oid = request.POST.get('oid')
    ototal = request.POST.get('ototal')
    print(float(ototal))
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = 1
    order.ototal = ototal
    order.save()
    print('111')
    return HttpResponse('ok')
