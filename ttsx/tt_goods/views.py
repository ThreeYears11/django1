from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# Create your views here.
from random import randint


def index(request):

    contex = {}
    for i in range(1,7):
        contex["goods_list%s"%i]=TypeInfo.objects.get(id=i).goodsinfo_set.all().order_by("-id")[0:4]
        contex["goods_list%s_hot"%i]=TypeInfo.objects.get(id=i).goodsinfo_set.all().order_by("gclick")[0:3]

    return render(request, "tt_goods/index.html", contex)


def list(request, id, id2, id3):

    # 获取商品类型
    goods_list1 = TypeInfo.objects.get(id=int(id))
    #排序规则
    goods_list=""
    if id3 == "1":
        # 获取该类型的所有产品类型
        goods_list = goods_list1.goodsinfo_set.all()
    elif id3 == "2":
        #按照人气排序
        goods_list = goods_list1.goodsinfo_set.all().order_by("gclick")
    elif id3 == "3":
        #按照价格排序
        goods_list = goods_list1.goodsinfo_set.all().order_by("gprice")


    # 该类产品每页显示１０条记录
    p = Paginator(goods_list, 10)
    # 该类产品按照页码显示
    page = p.page(int(id2))
    # 实现页码跳转
    pagelist = p.page_range

    page_sum = p.num_pages
    uplist = "/list%s/%s_%s"%(id,str(int(id2)-1),id3)
    nextlist = "/list%s/%s_%s"%(id,str(int(id2)+1),id3)
    # 获取新品推荐
    goods_new = goods_list.order_by('-id')[0:2]
    # 返回排序方式
    # sort_id = id3
    #返回当前页码
    # page_id = id2
    context = {
        "goods_list": page,
        "pagelist": pagelist,
        "uplist": uplist,
        "nextlist": nextlist,
        "goodlist1": goods_list1,
        "goods_new": goods_new,
        "listid": id,
        "sort_id":id3,
        "page_id":id2,
        "page_sum":page_sum,
    }

    return render(request, "tt_goods/list.html", context)

def reset(request):
    return HttpResponseRedirect('/')

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
        "listid": id,
    }
    resposn = render(request, "tt_goods/detail.html", context)
    resposn.set_cookie("goods_zjll",",".join(list))
    return resposn

def listx(request,id,id2=None):
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

    return render(request, "tt_goods/listx.html", context)

def listx_ajax(request):
    list = request.POST
    goods_list_index = list.get("goods_list_id")
    list_class_id = list.get("id")
    #找出种类
    goods_list1 = TypeInfo.objects.get(id=int(list_class_id))
    #找出该类的所有产品
    goods_list = goods_list1.goodsinfo_set.all()
    # 该类产品每页显示１０条记录
    p = Paginator(goods_list, 10)
    # 该类产品按照页码显示
    page = p.page(int(goods_list_index))

    context = {}
    n = 1
    for i in page:
        context["goods_id"+str(n)] = ''' < li >
     < a
     href = "detail%s.html" > < img
     src = "/static/images/%s" > < / a >
     < h4 > < a
     href = "detail%s.html" > %s < / a > < / h4 >
     < div

     class ="operate" >

     < span

     class ="prize" > ￥%s < / span >

     < span

     class ="unit" > %s / 500g < / span >

     < a
     href = "#"

     class ="add_goods" value="%s" title="加入购物车" > < / a >

    < / div >
    < / li >'''%(i.id,i.gpic,i.id,i.gtitle,i.gprice,i.gprice,i.id)
        n+=1

    print(context["goods_id1"])

    return JsonResponse(context)



