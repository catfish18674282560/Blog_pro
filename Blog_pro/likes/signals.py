from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from . models import LikeRecord


# 点赞消息通知
@receiver(post_save, sender=LikeRecord)
def send_likeRecord(sender, instance, **kwargs):
	if instance.content_type.model == 'blog':
		verb = '{}为你的博客点赞《{}》'.format(instance.user.get_nickName(), instance.content_object.title)
	elif instance.content_type.model == 'comment':
		verb = '{}为你的评论点赞"{}"'.format(instance.user.get_nickName(), instance.content_object.text)
	else:
		raise Exception('没有这个模型')
	# 获取用户
	recipient = instance.content_object.get_user()
	# 获取点赞模型url
	url = instance.content_object.get_url()
	notify.send(instance.user, recipient=recipient, verb=verb, url=url)

