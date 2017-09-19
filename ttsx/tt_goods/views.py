from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# Create your views here.
from random import randint


def index(request):
    # 获取水果
    goods_list1 = TypeInfo.objects.get(id=1).goodsinfo_set.filter(pk__in=[1, 182, 183, 184])
    print(goods_list1)
    # 海鲜水产
    goods_list2 = TypeInfo.objects.get(id=2).goodsinfo_set.filter(pk__in=[31, 47, 58, 59])
    # 猪牛羊肉
    goods_list3 = TypeInfo.objects.get(id=3).goodsinfo_set.filter(pk__in=[61, 89, 90, 63])
    # 禽类蛋品
    goods_list4 = TypeInfo.objects.get(id=4).goodsinfo_set.filter(pk__in=[91, 119, 120, 108])
    # 新鲜蔬菜
    goods_list5 = TypeInfo.objects.get(id=5).goodsinfo_set.filter(pk__in=[121, 122, 123, 149])
    # 速冻食品
    goods_list6 = TypeInfo.objects.get(id=6).goodsinfo_set.filter(pk__in=[179, 180, 172, 173])

    contex = {"goods_list1": goods_list1,
              "goods_list2": goods_list2,
              "goods_list3": goods_list3,
              "goods_list4": goods_list4,
              "goods_list5": goods_list5,
              "goods_list6": goods_list6,
              }
    # print(goods_list1)
    return render(request, "tt_goods/index.html", contex)


def list(request, id, id2=None):
    # if id == "1" :
    if id2 == None:
        id2 = 1
    # 获取商品类型
    goods_list1 = TypeInfo.objects.get(id=int(id))
    # 获取该类型的所有产品类型
    goods_list = goods_list1.goodsinfo_set.all()
    # 该类产品每页显示１０条记录
    p = Paginator(goods_list, 10)
    # 该类产品按照页码显示
    page = p.page(int(id2))
    # 获取页码跳转路径
    ids = "/list%s/" % id
    # 实现页码跳转
    pagelist = p.page_range
    uplist = ids + str(int(id2) - 1)
    nextlist = ids + str(int(id2) + 1)
    # 获取新品推荐
    goods_new = goods_list.order_by('-id')[0:2]

    context = {
        "goods_list": page,
        "pagelist": pagelist,
        "ids": ids,
        "uplist": uplist,
        "nextlist": nextlist,
        "goodlist1": goods_list1,
        "goods_new": goods_new,
        "listid": id,
    }

    return render(request, "tt_goods/list.html", context)


# def list_ajax(request):
#     id = request.GET.get("value")
#     id2 = request.GET.get("value2")
#
#     print(id,id2)
#
#     goods_list1 = TypeInfo.objects.get(id=int(id))
#     # 获取该类型的所有产品类型
#     goods_list = goods_list1.goodsinfo_set.all()
#     # 该类产品每页显示１０条记录
#     # print("duang2")
#     p = Paginator(goods_list, 10)
#     # 该类产品按照页码现实
#     page = p.page(int(id2))
#     # pagelist = p.page_range
#     # print(pagelist)
#
#     context={"page":id}
#     print(page)
#
#     return JsonResponse(context)

def reset(request):
    return HttpResponseRedirect('/')

goods_cookie_list = []
# def detail(request, id, id2):
#     # if id == "1":
#     # 获取当前商品类别
#     goods_class = TypeInfo.objects.get(id=int(id))
#     new_goods = goods_class.goodsinfo_set.all().order_by("-id")[0:2]
#     detail_goods = GoodsInfo.objects.get(id=id2)
#     detail_goods.gclick += 1
#     detail_goods.save()
#     # 设置ｃｏｏｋｉｅ
#     context = {
#         "new_goods": new_goods,
#         "detail_goods": detail_goods,
#         "goods_class": goods_class,
#     }
#
#     # flag = 1
#     # cookies = None
#     # goods_cookie_list = None
#     # try:
#     #     cookies = request.COOKIES["goods_id"]
#     # # except Exception as result:
#     # except:
#     #     flag = 0
#     #
#     #
#     # if(flag):
#     #     goods_cookie_list = cookies
#     #     print(goods_cookie_list)
#     #
#     #     while len(goods_cookie_list) <= 4:
#     #         goods_cookie_list.append(id2)
#     #
#     #     goods_cookie_list.append(id2)
#     #     goods_cookie_list.remove(goods_cookie_list[0])
#     #     # print(goods_cookie_list)
#     # else:
#     #     goods_cookie_list=[id2,]
#
#     resposn = render(request, "tt_goods/detail.html", context)
#     resposn.set_cookie("goods_id", id2)
#
#     return resposn

def detail(request, id, id2):
    # if id == "1":
    # 获取当前商品类别
    goods_class = TypeInfo.objects.get(id=int(id))
    new_goods = goods_class.goodsinfo_set.all().order_by("-id")[0:2]
    detail_goods = GoodsInfo.objects.get(id=id2)
    detail_goods.gclick += 1
    detail_goods.save()
    # 设置ｃｏｏｋｉｅ
    cookies = request.COOKIES.get("goods_zjll","")
    if cookies:
        list = cookies.split(",")
        if id2 in list:
            list.remove(id2)
        list.insert(0,id2)
        if len(list) > 5:
            list.pop()
    else:
        list = id2
    context = {
        "new_goods": new_goods,
        "detail_goods": detail_goods,
        "goods_class": goods_class,
    }
    resposn = render(request, "tt_goods/detail.html", context)
    resposn.set_cookie("goods_zjll",",".join(list))
    return resposn
