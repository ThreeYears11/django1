from django.shortcuts import render
from .models import *
from .models import OrderInfo


# Create your views here.
def place_order(request):
    order_all = OrderInfo.objects.all()
    content = {'addr': order_all}
    return render(request, "tt_order/place_order.html", content)
