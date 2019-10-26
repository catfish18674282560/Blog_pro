from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from notifications.models import Notification

# 全部消息设置为已读
def notification_all_read(request):
	request.user.notifications.mark_all_as_read()
	return redirect(reverse('my_notifications'))

# 删除全部已读消息
def notification_all_delete(request):
	Notification.objects.filter(unread=False).delete()
	return redirect(reverse('my_notifications'))

# 单个未读消息设置为已读
def notification_read(request,notification_id):
	notification = get_object_or_404(Notification, pk=notification_id) 		# 相当于get()查询，如果获取不到则抛出404错误
	notification.unread = False
	notification.save()
	# 从data字段获取保存的实例url地址
	return redirect(notification.data['url'])

# 消息
def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)
