from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from notifications.signals import notify
from django.contrib.auth import get_user_model
from .models import MyUser


User = get_user_model()
# 新用户注册消息提醒
@receiver(post_save, sender=User)
def send_user(sender, instance, **kwargs):
	if kwargs['created'] == True:
		recipient = User.objects.filter(is_superuser=True) 			# 筛选出所有超级管理员
		verb = '有新用户创建了!'
		# 获取个人资料url
		url = reverse('personal_data')
		notify.send(instance, recipient=recipient, verb=verb, url=url)