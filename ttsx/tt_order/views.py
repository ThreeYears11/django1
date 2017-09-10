from django.shortcuts import render
from django.http import HttpResponse
# from .models import *
from .models import OrderInfo, OrderDetailInfo


# Create your views here.
def place_order(request):
    get = request.GET
    id = get.get('id')
    goods = OrderDetailInfo.objects.all()
    order = OrderInfo.objects.get(pk=1)
    phone = order.user.useraddressinfo_set.all()[0]
    content = {'user': order, 'phone': phone, 'goods': goods}
    return render(request, "tt_order/place_order.html", content)


def order_add(request):
    a = OrderInfo()
    a.user_id = 1
    a.ototal = '123.11'
    a.oaddress = 'adffaf'
    a.save()
    return HttpResponse('ok')
