#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

# Create your views here.

from datetime import date
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from . models import *
from hashlib import *
from PIL import Image, ImageDraw, ImageFont
from pymysql import *
from django.conf import settings
from django.core.mail import send_mail
from . import task


# Create your views here.
def register(request):
    return render(request,'tt_user/register.html')

def register1(request):
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    email = dict.get('email')
    s1 = sha1()
    s1.update(upwd.encode())
    sha_pwd = s1.hexdigest()
    userinfo = UserInfo()
    userinfo.uname = uname
    userinfo.upwd = sha_pwd
    userinfo.uemail = email
    userinfo.save()
    task.sendmail.delay(userinfo.id,email)
    # return redirect('/user/login/')
    return HttpResponse('用户注册成功，请到邮箱中激活')

def active(request,uid):
    user = UserInfo.objects.get(id = uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功, <a href="/user/login/">点击登录</a>')


def login(request):
    return render(request,'tt_user/login.html')

def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画布对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    from io import BytesIO
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def yzm(request):
    return render(request,'tt_user/register.html')
def yzm2(request):
    yzm_value = request.GET.get('yzm_value')
    print(yzm_value)
    if yzm_value == request.session['verifycode']:
        return JsonResponse({'pass':'ok'})
    else:
        return JsonResponse({'pass':'no'})

def check_user(request):
    name = request.GET.get('user_name')
    psw = UserInfo.objects.filter(uname=name)
    if psw:
        return JsonResponse({'check':'yes'})
    else:
        return JsonResponse({'check':'no'})

def check_email(request):
    email = request.GET.get('email')
    oEmail = UserInfo.objects.filter(uemail=email)
    if oEmail:
        return JsonResponse({'check':'yes'})
    else:
        return JsonResponse({'check':'no'})

def check_login(request):
    # 这个函数只要判断用户名存不存在
    name = request.GET.get('name')

    # 这个用户名在不在数据库 , 也就是说这个用户名存不存在
    oName = UserInfo.objects.filter(uname = name)

    # 如果存在
    # return JsonResponse({'result': '1'}) --> 代表存在
    if oName:
        return JsonResponse({'result':'1'})

    # 如果不存在
    # return JsonResponse({'result': '０'}) --> 代表不存在
    else:
        return JsonResponse({'result':'0'})

def login_cookie(request):
    if request.COOKIES['name']:
        print(request.COOKIES['name'])
        return JsonResponse({'cookie':request.COOKIES['name']})
    else:
        return JsonResponse({'cookie':'no'})

def site(request):
    dict = request.POST
    name = dict.get('user_name')
    site_area = dict.get('site_area')
    phone = dict.get('phone')
    id = dict.get('adid')
    print(id)
    if id=='':

        # 取出当前登录用户的cookie的名字
        uname = request.COOKIES.get('name')
        # 用名字取出对应的对象
        userinfo = UserInfo.objects.filter(uname=uname)
        useraddr = UserAddressInfo()
        useraddr.uname = name
        useraddr.uaddress = site_area
        useraddr.uphone = phone
        # 用户地址的外键属性等于用户对象
        useraddr.user = userinfo[0]
        useraddr.save()
        return redirect('/user/show/')
    # xiugai
    else:
        useraddinfo = UserAddressInfo.objects.get(id=id)
        useraddinfo.uname = name
        useraddinfo.uaddress = site_area
        useraddinfo.uphone = phone
        useraddinfo.save()
        data = '<span style="display: none">1</span>&nbsp;%s&nbsp;&nbsp;&nbsp;(%s&nbsp;收)&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;<a href="#" class="a">修改</a><label></label>' % (
        site_area, name, phone)
        request.session['data'] = data
        return redirect('/user/show/')

    # return render(request,'tt_user/user_center_site.html')

def show(request):
    return render(request,'tt_user/user_center_site.html')

def show_user(request):
    name = request.COOKIES.get('name')
    return JsonResponse({'name':name})

def add_addr(request):
    print('青青')
    name = request.COOKIES.get('name')
    useraddr = UserAddressInfo.objects.filter(user__uname=name)
    list = []
    for addr in useraddr:
        list.append({'name':addr.uname,'addr':addr.uaddress,'num':addr.uphone,'id':addr.id})
    return JsonResponse({'list':list})

def current(request):
    data = request.GET.get('data')
    request.session['data'] = data
    print(data)
    request.session.set_expiry(None)
    return JsonResponse({'isok':'true'})

def site_cur(request):
    data = request.session.get('data')
    return JsonResponse({'data':data})


def xiugai(request):
    userad = request.GET
    ad_id = userad.get('ad_id')
    useraddinfo = UserAddressInfo.objects.get(id=ad_id)
    uname = useraddinfo.uname
    uaddress = useraddinfo.uaddress
    uphone = useraddinfo.uphone
    return  JsonResponse({'uuname':uname,'uaddress':uaddress,'uphone':uphone})

def info(request):
    return render(request,'tt_user/user_center_info.html')

def denglu(request):
    dict = request.POST
    name = dict.get('username')
    pwd = dict.get('pwd')
    user = UserInfo.objects.filter(uname=name)
    if user:
        s1 = sha1()
        s1.update(s1.encode('utf-8'))

def order(request):
    return render(request,'tt_user/user_center_order.html')