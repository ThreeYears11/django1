from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .models import OrderInfo


# Create your views here.
def place_order(request):
    # id = 1
    # order = OrderInfo.objects.get(user_id=1)
    # content = {'user': order}
    return render(request, "tt_order/place_order.html")


def order_add(request):
    a = OrderInfo()
    a.user_id = 1
    a.ototal = '123.11'
    a.oaddress = 'adffaf'
    a.save()
    return HttpResponse('ok')
