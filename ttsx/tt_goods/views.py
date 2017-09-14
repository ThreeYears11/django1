from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# Create your views here.
from random import randint
def index(request):
    #获取水果
    goods_list1 = TypeInfo.objects.get(id=1).goodsinfo_set.all()[::-1][0:4]
    #海鲜水产
    goods_list2 = TypeInfo.objects.get(id=2).goodsinfo_set.all()[::-1][0:4]
    #猪牛羊肉
    goods_list3 = TypeInfo.objects.get(id=3).goodsinfo_set.all()[::-1][0:4]
    # 禽类蛋品
    goods_list4 = TypeInfo.objects.get(id=4).goodsinfo_set.all()[::-1][0:4]
    # 新鲜蔬菜
    goods_list5 = TypeInfo.objects.get(id=5).goodsinfo_set.all()[::-1][0:4]
    # 速冻食品
    goods_list6 = TypeInfo.objects.get(id=6).goodsinfo_set.all()[::-1][0:4]

    contex = {"goods_list1": goods_list1,
              "goods_list2": goods_list2,
              "goods_list3": goods_list3,
              "goods_list4": goods_list4,
              "goods_list5": goods_list5,
              "goods_list6": goods_list6,
              }
    print(goods_list1)
    return render(request,"tt_goods/index.html",contex)

def list(request,id,id2=None):
    # if id == "1" :
    if id2 == None:
        id2 = 1
    #获取商品类型
    goods_list1 = TypeInfo.objects.get(id=int(id))
    #获取该类型的所有产品类型
    goods_list = goods_list1.goodsinfo_set.all()
    #该类产品每页显示１０条记录
    p = Paginator(goods_list, 10)
    #该类产品按照页码现实
    page =p.page(int(id2))
    #获取页码跳转路径
    ids = "/list%s/"%id
    #获取
    pagelist = p.page_range
    uplist = ids+str(int(id2)-1)
    nextlist = ids+str(int(id2)+1)
    #获取新品推荐
    goods_new = goods_list[::-1][0:2]
    # goods_new2 = goods_list[::-1][2]



    context = {
               "goods_list":page,
               "pagelist":pagelist,
               "ids":ids,
               "uplist":uplist,
               "nextlist":nextlist,
               "goodlist1":goods_list1,
               "goods_new":goods_new,
               "listid":id,
               }

    return render(request,"tt_goods/list.html",context)

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


def detail(request,id,id2):
    # if id == "1":
    goods_class = TypeInfo.objects.get(id=int(id))
    new_goods = goods_class.goodsinfo_set.all()[::-1][0:2]
    detail_goods = GoodsInfo.objects.get(id=id2)

    context = {
                "new_goods":new_goods,
                "detail_goods":detail_goods,
                "goods_class":goods_class,
              }
    return render(request,"tt_goods/detail.html",context)


