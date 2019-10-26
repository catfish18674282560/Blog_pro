"""Blog_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')), # 框架消息映射
    path('ckeditor/',include('ckeditor_uploader.urls')),        # 富文本编辑器
    path('', views.index),                                      # 粒子特效
    path('index/', views.home, name='home'),                    # 博客主页
    path('admin/', admin.site.urls),                            # 后台管理
    path('blog/', include('blog_app1.urls')),                   # 博客映射路由
    path('comment/', include('comment.urls')),                  # 评论映射路由
    path('likes/', include('likes.urls')),                      # 点赞映射路由
    path('user/', include('user.urls')),
    path('my_notifications/', include('my_notifications.urls')),# 消息映射
    path('word_seaech/', views.word_seaech, name='word_seaech'),# 站内搜索
]
# 判断如果为开发模式，手动设置media文件搜索路径
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
