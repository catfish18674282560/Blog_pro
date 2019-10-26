import time
import string
import random
import smtplib                                                  # 邮件
import json
from urllib.parse import urlencode,parse_qs
from urllib.request import urlopen
from django.urls import reverse                                 # url反向查询
from django.http import JsonResponse
from django.core.mail import send_mail                          # 发送邮件
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from .forms import LoginForm, RegForm, ChangeNickNameForm, ChangeEmailForm, ChangePassword, ForgetPassword, BindQQForm
from .models import OAuthRelationship


# 获取自定义用户模型对象
User = get_user_model()

# 用户登录
def user_login(request):
    if request.method == "POST":                                # 判断是否是POST请求
        form = LoginForm(request.POST)                    # 绑定数据到表单中
        if form.is_valid():                               # 判断表单数据是否通过验证
            user = form.cleaned_data['user']              # 获取保存在cleaned_data字典中通过验证的用户
            login(request, user)                                # 登陆该用户
            return redirect(request.GET.get('from', reverse('home')))# 获取GET请求发送的url地址
    else:
        form = LoginForm()                                # 如果是GET请求则保存一个空表单数据

    context = {}
    context['form'] = form
    context['title'] = '用户登录'
    context['button_str'] = '登录'
    return render(request, 'login.html', context)


# 弹出登陆框
def login_up(request):
    form = LoginForm(request.POST)
    data = {}
    if form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        data['status'] = '200'
        data['success'] = '登录成功'
    else:
        data['status'] = '500'
        data['error'] = '账号或密码错误'
    return JsonResponse(data)


# 用户注册
def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST, request=request)                          # 绑定表单提交数据到RegForm表单类
        if reg_form.is_valid():                                                    # 表单验证
            email = reg_form.cleaned_data['email']
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password_again']
            user = User.objects.create_user(username=username, password=password, email=email)  # 重写User类指定字段
            user.save()

            user = authenticate(username=username, password=password)               # 验证指定用户名、密码
            login(request, user)                                                    # 登陆该注册用户
            del request.session['register_code']                                    # 从session会话中删除保存的验证码
            del request.session['code_time']
            return redirect(request.GET.get('from', reverse('home')))               # 注册成功跳转到上一个页面
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    context['title'] = '注册'
    context['button_str'] = '注册'
    return render(request, 'register.html', context)


# 退出登陆
def exit_login(request):
    logout(request)
    return redirect(request.GET.get('from',reverse('home')))            # 跳转到来到该页面之前的页面

# 个人资料
def personal_data(request):
    # 获取QQ头像 100x100
    img = OAuthRelationship.objects.get(user=request.user,oauth_type=0).portrait_img_url
    context = {}
    context['img'] = img
    return render(request, 'personal_data.html', context)

# 修改昵称
def change_NickName(request):
    context = {}
    if request.method == 'POST':
        from_to = redirect(request.GET.get('from',reverse('home')))     # 获取进入到该页面前url地址
        user = request.user                                             # 获取当前用户对象
        form = ChangeNickNameForm(request.POST,user=user)               # 绑定表单数据，并将当前用户对象传入
        if form.is_valid():                                             
            nick_name = form.cleaned_data['changeNickname']             # 获取通过验证表单数据
            user.nickName = nick_name                                   # 修改昵称
            user.save()                                                 # 保存
            return from_to                                              # 修改成功后跳转的上一页面
    else:
        form = ChangeNickNameForm()
    
    context['form'] = form
    context['title'] = '修改昵称'
    context['button_str'] = '修改'
    return render(request, 'change_NickName.html', context)

# 修改邮箱
def change_Email(request):
    if request.method == 'POST':
        from_to = redirect(request.GET.get('from',reverse('home')))
        form = ChangeEmailForm(request.POST,request=request)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()

            del request.session['change_Email_code']        # 修改完邮箱删除验证码
            del request.session['code_time']                # 修改完邮箱删除发送验证码时间
            return from_to
    else:
        form = ChangeEmailForm()

    context = {}
    context['form'] = form
    context['title'] = '修改邮箱'
    context['button_str'] = '修改'
    context['get_verification'] = '发送验证码'
    return render(request, 'change_Email.html', context)

# 修改密码
def change_Password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST,user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            logout(request)                                 # 退出登录
    else:
        form = ChangePassword()
    context = {}
    context['form'] = form
    context['title'] = '修改密码'
    context['button_str'] = '修改'
    return render(request, 'change_Password.html', context)

# 忘记密码
def forget_Password(request):
    if request.method == 'POST':
        form = ForgetPassword(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['again_password']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            del request.session['forget_Password_code']     # 删除session中保存的验证码
            return redirect(reverse('home'))                # 跳转首页
    else:
        form = ForgetPassword()
        
    context = {}
    context['form'] = form
    context['title'] = '忘记密码'
    context['get_verification'] = '发送验证码'
    context['button_str'] = '登录'
    return render(request, 'forget_Password.html', context)

# 发送邮件
def send_Email(request):
    data = {}
    def ResponseError(status, error):               # 发送成功相应邮件
        data['status'] = status
        data['error'] = error
        return data
    def ResponseSuccess(status, success):           # 发送失败相应邮件
        data['status'] = status
        data['success'] = success
        return data

    email = request.GET['email']                                # 获取邮箱
    if email != '':                                             # 判断邮箱是否为空
        list_code = random.sample(string.ascii_letters + string.digits, 4)  # 随机生成4位字母+数字验证码
        code = ''.join(list_code)                               # 将列表变为字符串
        now = int(time.time())                                  # 获取新时间戳，取整
        code_time = request.session.get('code_time',0)          # 获取旧时间戳或0
        if now - code_time > 30:                                # （新时间戳 - 旧时间戳）他们的差小于30则说明在30秒之内
            try:
                send_mail(                                      # 发送邮件
                    '帅哥博客验证码',
                    '验证码: ' + code,
                    '728677713@qq.com',
                    [email],
                    fail_silently=False
                )
            except smtplib.SMTPException:
                ResponseError('500','发送失败')
            else:
                code_type = request.GET['code_type']
                request.session[code_type] = code                # 保存验证码，key为前端传递的值
                request.session['code_time'] = now               # 保存新时间戳
                ResponseSuccess('200','发送成功')
        else:
            error_str = '请%s秒后发送' % ((request.session.get('code_time', 0) - now) + 30)  # 发送验证码倒计时
            ResponseError('500',error_str)
    else:
        ResponseError('500','请填写邮箱')
    return JsonResponse(data)

# QQ第三方快捷登录参数获取
def login_by_qq(request):
    code = request.GET['code']
    state = request.GET['state']
    # 获取access_token
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.QQ_APP_ID,
        'client_secret': settings.QQ_APP_KEY,
        'code': code,
        'redirect_uri': settings.QQ_URL,
    }
    response = urlopen('https://graph.qq.com/oauth2.0/token?' + urlencode(data))
    data = response.read().decode()
    access_token = parse_qs(data)['access_token'][0]
    # 获取openid
    response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=' + access_token)
    data = response.read().decode()
    openid = json.loads(data[10:-4])['openid']

    # 获取当前QQ详情资料
    data = {
        'access_token': access_token,
        'oauth_consumer_key': settings.QQ_APP_ID,
        'openid': openid,
    }
    response = urlopen('https://graph.qq.com/user/get_user_info?' + urlencode(data))
    data = response.read().decode()
    request.session['qq_head_100x100_img'] = json.loads(data)['figureurl_qq_2']

    # 判断数据库中是否已存在该openid
    if OAuthRelationship.objects.filter(appid=openid).exists():
        # 存在则登陆
        user = OAuthRelationship.objects.get(appid=openid).user
        login(request,user)
        return redirect(reverse('home'))
    else:
        # 不存在则绑定QQ
        request.session['openid'] = openid
        return redirect(reverse('bind_qq'))

# 绑定QQ
def bind_qq(request):
    if request.method == 'POST':
        bind_qq_form = BindQQForm(request.POST)
        if bind_qq_form.is_valid():
            user = bind_qq_form.cleaned_data['user']
            # 记录该用户的QQ第三方关联
            relationship = OAuthRelationship()
            relationship.user = user
            relationship.appid = request.session.pop('openid')
            relationship.oauth_type = 0
            relationship.portrait_img_url = request.session.pop('qq_head_100x100_img')
            relationship.save()
            #登陆
            login(request, user)
            return redirect(reverse('home'))
    else:
        bind_qq_form = BindQQForm()

    context = {}
    context['form'] = bind_qq_form
    context['title'] = '绑定QQ'
    context['button_str'] = '绑定并登陆'
    return render(request, 'bind_qq.html', context)
