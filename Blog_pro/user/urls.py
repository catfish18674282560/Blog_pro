from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),                    # 登陆
    path('login_up/', views.login_up, name='login_up'),                     # 弹出登录框
    path('exit_login/', views.exit_login, name='exit_login'),               # 退出登录
    path('register/', views.register, name='register'),                     # 注册
    path('personal_data/', views.personal_data, name='personal_data'),      #个人资料
    path('change_NickName/', views.change_NickName, name='change_NickName'), # 修改昵称
    path('change_Email/',views.change_Email, name='change_Email'),          # 修改邮箱
    path('send_Email/',views.send_Email, name='send_Email'),                # 发送邮件
    path('change_Password/', views.change_Password, name='change_Password'),# 修改密码
    path('forget_Password/', views.forget_Password, name='forget_Password'),# 忘记密码
    path('login_by_qq', views.login_by_qq, name='login_by_qq'),             # QQ快捷登录参数获取
    path('bind_qq', views.bind_qq, name='bind_qq'),                         # 绑定QQ
]
