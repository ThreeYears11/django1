#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

# Create your views here.

from datetime import date
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse,JsonResponse

from .user_decorators import *
from . models import *
from hashlib import *
from PIL import Image, ImageDraw, ImageFont
from pymysql import *
from django.conf import settings
from django.core.mail import send_mail
from . import task
from tt_order.models import *
from tt_goods.models import *
from django.core.paginator import Paginator


# Create your views here


# 显示登录页
# 注册页面
def register(request):
    return render(request,'tt_user/register.html')

# 获取注册信息并保存到数据库
def register1(request):
    # 判断是否是在地址栏直接敲回车的ｇｅｔ请求，如果是就回到注册页
    if request.method == 'GET':
        return redirect('/user/register/')
    # 取出注册提交的数据
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    email = dict.get('email')
    # 查询注册名是否已存在
    username = UserInfo.objects.filter(uname=uname)
    # 查询注册邮箱是否已存在
    useremail = UserInfo.objects.filter(uemail=email)

    # 名字和邮箱有一个存在的话,就注册不成功并返回注册页提示
    if username or useremail:
        if username:
            return render(request,'tt_user/register.html',{'is_name':1})
        else:
            return render(request, 'tt_user/register.html', {'is_email': 1})
    # 数据库没有相同的用户名或者邮箱就注册成功并把数据保存在数据库里面
    else:
        s1 = sha1()
        s1.update(upwd.encode())
        sha_pwd = s1.hexdigest()
        # 创建对象把数据保存在数据库里面
        userinfo = UserInfo()
        userinfo.uname = uname
        userinfo.upwd = sha_pwd
        userinfo.uemail = email
        userinfo.save()

        # task模块里面的sendmail方法，用delay的话就可以把任务添加至队列实现异步，才能从队列里面调度出来执行，否则不能
        task.sendmail.delay(userinfo.id,email)
        # return redirect('/user/login/')
        return HttpResponse('用户注册成功，请到邮箱中激活')

# 点击激活邮箱并且把数据库isActive改为true
def active(request,uid):
    user = UserInfo.objects.get(id = uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功, <a href="/user/login/">点击登录</a>')

# 登录并显示记住用户名，没有记住的话显示空
def login(request):
    name = request.COOKIES.get('name','')
    context = {'name':name}
    return render(request,'tt_user/login.html',context)

# 做成验证码函数
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

# 显示验证码图片
def yzm(request):
    return render(request,'tt_user/register.html')

# 判断验证码是否正确
def yzm2(request):
    yzm_value = request.GET.get('yzm_value')
    print(yzm_value)
    if yzm_value == request.session['verifycode']:
        return JsonResponse({'pass':'ok'})
    else:
        return JsonResponse({'pass':'no'})

# 注册时检查用户是否存在
def check_user(request):
    name = request.GET.get('user_name')
    username = UserInfo.objects.filter(uname=name)
    if username:
        return JsonResponse({'check':'yes'})
    else:
        return JsonResponse({'check':'no'})

# 注册时检查邮箱是否存在
def check_email(request):
    email = request.GET.get('email')
    count = UserInfo.objects.filter(uemail=email).count()
    if count:
        return JsonResponse({'check':'yes'})
    else:
        return JsonResponse({'check':'no'})

# 登录时检查用户是否存在
def check_login(request):
    # 这个函数只要判断用户名存不存在
    name = request.GET.get('name')

    # 这个用户名在不在数据库 , 也就是说这个用户名存不存在
    oName = UserInfo.objects.filter(uname = name)

    # 如果存在
    # return JsonResponse({'result': '1'}) --> 代表存在
    if oName[0]:
        return JsonResponse({'result':'1'})

    # 如果不存在
    # return JsonResponse({'result': '０'}) --> 代表不存在
    else:
        return JsonResponse({'result':'0'})

# 登录cookie 暂时不知道哪里调用这个视图
def login_cookie(request):
    if request.COOKIES['name']:
        return JsonResponse({'cookie':request.COOKIES['name']})
    else:
        return JsonResponse({'cookie':'no'})

# 收货地址的数据提交的视图，如果id没有的话就增加，否则就修改
def site(request):
    dict = request.POST
    name = dict.get('user_name')
    site_area = dict.get('site_area')
    phone = dict.get('phone')
    id = dict.get('adid')
    cur_id = dict.get('cur_site_id')
    # 如果没有id证明是添加收货地址
    if id=='':
        # 不能用cookies，因为如果用户不勾上记住用户名，cookies是没有名字的
        # 这时就取不到数据库里面的数据了取出当前登录用户的cookie的名字
        # uname = request.COOKIES.get('name')

        uname = request.session.get('uname')
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
    # 如果有id就证明是修改地址
    else:
        # 用id找出对应的地址对象并修改完保存
        useraddinfo = UserAddressInfo.objects.get(id=id)
        useraddinfo.uname = name
        useraddinfo.uaddress = site_area
        useraddinfo.uphone = phone
        useraddinfo.save()
        # 如果当前地址和修改地址是同一个,就把修改好的地址存到session
        print(id,cur_id)
        print('相等吗')
        if id == cur_id:
            # 把字符串拼接成html格式存在session
            data = '<span style="display: none">%s</span>&nbsp;%s&nbsp;&nbsp;&nbsp;(%s&nbsp;收)&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;<a href="#" class="a">修改</a><label></label>' % (
            id,site_area, name, phone)
            request.session['data'] = data
            print(data)
            print('session')
            return redirect('/user/show/')

        else:
            # 如果存的不是同一个ｉｄ，session的值则不变
            return redirect('/user/show/')

# 显示用户中心
@is_login
def info(request):
    # 取出session中uname值传到页面备用
    uid = request.session.get('uid')
    # 取到当前用户的邮箱
    current_user = UserInfo.objects.filter(id=uid)
    name = current_user[0].uname
    email = current_user[0].uemail
    # 取出最近浏览的cookies
    cookies = request.COOKIES.get("goods_zjll", "")
    id_list = cookies.split(",")
    good_list = []
    context = {'gList': good_list, 'uname': name, 'email': email}
    # 如果没有cookie
    if cookies == '':
        return render(request, 'tt_user/user_center_info.html', context)
    else:
        for g in id_list:
            gid = int(g)
            good = GoodsInfo.objects.filter(id=gid)
            good_list.append(good[0])
        return render(request, 'tt_user/user_center_info.html', context)

# 显示收货地址
@is_login
def show(request):
    return render(request,'tt_user/user_center_site.html')


# 用户中心中的我的订单界面
@is_login
def order(request, pIndex):
    uid = request.session.get('uid')
    orders_sort = OrderInfo.objects.filter(user_id=uid)
    if pIndex == '':
        pIndex = '1'
    if len(orders_sort) == 0:
        context = {'empty': 'yes'}
    else:
        orders = orders_sort[::-1]
        order_no_pay = OrderDetailInfo.objects.filter(order__user_id=uid).filter(order__oIsPay=0)
        order_pay = OrderDetailInfo.objects.filter(order__user_id=uid).filter(order__oIsPay=1)

        # 分页
        paginator = Paginator(orders, 2)
        pindexs = int(pIndex)
        page = paginator.page(pindexs)
        context = {'orders': page, 'order_no_pay': order_no_pay, 'order_pay': order_pay, 'empty': 'no', 'pIndex': pindexs}
    return render(request,'tt_user/user_center_order.html', context)


# 把登录的用户名对应的所有地址添加到已保存地址并显示
def add_addr(request):
    # 不能用cookies，因为如果用户不勾上记住用户名，cookies是没有名字的
    # 这时就取不到数据库里面的数据了取出当前登录用户的cookie的名字
    # name = request.COOKIES.get('name')
    name = request.session.get('uname')
    useraddr = UserAddressInfo.objects.filter(user__uname=name)
    list = []
    for addr in useraddr:
        list.append({'name':addr.uname,'addr':addr.uaddress,'num':addr.uphone,'id':addr.id})
    return JsonResponse({'list':list})

# 把当前地址添加到session
def current(request):
    data = request.GET.get('data')
    request.session['data'] = data
    request.session.set_expiry(None)
    return JsonResponse({'isok':'true'})

# 从session取出地址显示为当前地址
def site_cur(request):
    data = request.session.get('data')
    return JsonResponse({'data':data})

# 修改用户地址
def xiugai(request):
    userad = request.GET
    # 接收用户传过来的当前点击修改的id
    ad_id = userad.get('ad_id')
    # 查找出对应id的地址对象
    useraddinfo = UserAddressInfo.objects.get(id=ad_id)
    # 把此对象的值赋给变量
    uname = useraddinfo.uname
    uaddress = useraddinfo.uaddress
    uphone = useraddinfo.uphone
    # 把从数据库获取出来的值通过json传送过去
    return  JsonResponse({'uuname':uname,'uaddress':uaddress,'uphone':uphone})

# 登录页面
def denglu(request):
    # 如果在地址栏敲回车的get请求，就重定向到登录页
    if request.method == "GET":
        return redirect('/user/login/')
    # 接收从login页面点击登录提交过来的用户名和密码
    dict = request.POST
    name = dict.get('username')
    pwd = dict.get('pwd')
    remeber = dict.get('remeber','0')# 客户选中记住用户就是1,否则就是默认值0
    yzm = dict.get('yzm_value')# 接收用户在输入框中输入的验证码

    # 上下文拼接,error 都默认值为0
    context = { 'name': name, 'upwd': pwd, 'uname_error': 0, 'upwd_error': 0, 'yzm_error':0}

    # 如果用户输入的验证码不等于session存着的验证码，表示用户输入验证码有误
    if yzm != request.session['verifycode']:
        context['yzm_error']=1# 给上下文同样的键赋值为１
        return render(request,'tt_user/login.html',context)# 返回登录页面
    user = UserInfo.objects.filter(uname=name)# 验证码正确从数据库中查找对应用户名
    if user:  # 如果此用户名已注册
        s1 = sha1()# 那么就对用户输入的密码进行加密
        s1.update(pwd.encode('utf-8'))
        spwd = s1.hexdigest()
        if spwd == user[0].upwd:# 用户输入的密码如果正确
            if user[0].isActive:# 如果此用户已激活

                # 则重定向到用户上次点击的页面
                # redirect是HttpResponseRedirect的简写因为继承与类HttpResponse所以返回的也是response对象
                response = redirect(request.session.get('url_path','/'))
                # 记住用户名,如果用户勾上记住用户名
                if remeber == '1':
                    # 则把此用户名存在cookie中
                    response.set_cookie('name',name,expires=14*24*60*60)
                else:  # 否则给cookie同样的键附上一个空字符串，而且过期时间设为负值，则浏览器马上删除cookie
                    response.set_cookie('name','',expires=-1)
                # 登录成功把用户的id和名字存在session中
                request.session['uid'] = user[0].id
                request.session['uname'] = name
                return response
            else:  # 如果此用户没激活则给用户显示如下文字
                return HttpResponse('账户未激活，请前往注册邮箱激活')
        else:  # 如果用户密码不正确则返回把键的值改为１并回到登录页
            context['upwd_error'] = 1
            return render(request,'tt_user/login.html',context)
    else:  # 如果此用户名没有注册则把键的值改为１并回到登录页
        context['uname_error'] = 1
        return render(request,'tt_user/login.html',context)

# 退出即清除session数据
def logout(request):
    # 清除会话数据，在存储中删除会话的整条数据
    request.session.flush()
    return redirect('/')

# 当输入框失去焦点时判断验证码是否正确
def check_yzm(request):
    yzm = request.GET.get('yzm')
    if yzm == request.session.get('verifycode'):
        return JsonResponse({'yzm':'ok'})
    else:
        return JsonResponse({'yzm':'no'})





