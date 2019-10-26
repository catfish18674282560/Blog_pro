from django.urls import path
from . import views


urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),			# 获取前端请求数据并创建评论
]
