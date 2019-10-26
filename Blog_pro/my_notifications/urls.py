from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_notifications, name='my_notifications'),      								# 消息
    path('my_notifications/<int:notification_id>', views.notification_read, name='notification_read'), 	# 单个未读消息设置为已读	
    path('notification_all_read/', views.notification_all_read, name='notification_all_read'),  	# 全部设置为已读消息
    path('notification_all_delete/', views.notification_all_delete, name='notification_all_delete'), # 删除全部已读消息 								# ajax请求获取未读消息数量
]