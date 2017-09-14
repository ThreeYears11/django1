#coding=utf-8
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

def denglu(request):
    # 密码对不对
    dict = request.POST
    pwd = dict.get('pwd')
    name = dict.get('username')
    s1 = sha1()
    s1.update(pwd.encode())
    s_pwd = s1.hexdigest()

    #　根据用户名在数据库找密码
    user = UserInfo.objects.filter(upwd=s_pwd)
    if user:
        table_pwd = user[0].upwd
        # 比对密码是否正确
        if s_pwd == table_pwd:
            # 如果密码正确
            response = render(request,'tt_goods/index.html',{'name':name})
            checkbox = dict.get('checked')
            if checkbox == None:
                response.delete_cookie('name')
            else:
                response.set_cookie('name',name, expires=15*24*60*60)
            return response
            # return render(request,'tt_goods/index.html',{'name':name})

    else: # 如果密码不正确
        # return redirect('/user/login/')
        return render(request, 'tt_user/login.html',{'no':'密码有误'})


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
    if name or site_area or phone != None:
        useraddr = UserAddressInfo()
        useraddr.uname = name
        useraddr.uaddress = site_area
        useraddr.uphone = phone
        useraddr.save()
        request.session['name'] = name
        request.session['site_area'] = site_area
        request.session['phone']= phone
        request.session.set_expiry(None)
    return redirect('/user/show/')

def show(request):
    name = request.session.get('name')
    site_area = request.session.get('site_area')
    phone = request.session.get('phone')
    str = '%s (%s) %s' % (site_area, name, phone)
    return render(request, 'tt_user/user_center_site.html', {'str': str})
#
# def site_list(request):
#     useraddr = UserAddressInfo.objects.all()
#     if useraddr:
#         list = []
#         for i in useraddr:
#             name = i.uname
#             addr = i.uaddress
#             phone = i.uphone
#             str = '%s (%s) %s' % (addr, name, phone)
#             list.append({'str':str})
#     else:
#         list = ''
#         # context = {'list':list}
#         # render(request,'tt_user/user_center_site.html',context)
#     return JsonResponse({'list':list})