import threading
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Comment



@receiver(post_save, sender=Comment)
def send_notifications(sender, instance, **kwargs):
	if instance.content_type.model == 'blog':
		if instance.reply_to:
			# 回复
			recipient = instance.reply_to
			verb = '{}回复了你的评论"{}"'.format(instance.user.get_nickName(), instance.parent.text)
		else:
			# 评论
			recipient = instance.content_object.author
			verb = '{}评论了你的博客《{}》'.format(instance.user.get_nickName(), instance.content_object.title)
		# 获取博客url并拼接元素ID值设置锚点
		url = instance.content_object.get_url() + '#comment_' + str(instance.pk)
		notify.send(instance.user, recipient=recipient, verb=verb, url=url)
	else:
		raise Exception('没有该模型')


# 定义发送邮件多线程
class SendEmail_Thread(threading.Thread):
	def __init__(self,title,text,email,mail_to):
		self.title = title
		self.email = email
		self.text = text
		self.mail_to = mail_to
		threading.Thread.__init__(self)
	def run(self):
		code = send_mail(                                          # 发送邮件
			self.title,
			'',
			self.email,
			[self.mail_to],
			html_message = self.text,
		)
		if code:
			print('发送成功',code)
		else:
			print('发送失败',code)

@receiver(post_save, sender=Comment)
def send_email(sender, instance, **kwargs):
	if instance.reply_to is None:
		# 评论
		title='有人评论你的博客（%s）' % instance.content_object.title
		mail_to=instance.content_object.get_email()
	else:
		# 回复
		title='有人回复你的评论'        
		mail_to=instance.reply_to.email
		
	# 判断邮箱是否不为空	
	if mail_to != '':	
		email=settings.EMAIL_HOST_USER
		context = {}
		context['text'] = instance.text
		context['link'] = instance.content_object.get_url()
		text = render_to_string('send_mail_html/send_mail.html',context)  	# 通过render_to_string()函数返回指定HTML模板中HTML代码字符串
		thread = SendEmail_Thread(title,text,email,mail_to)               	# 创建线程
		thread.start()
		#thread.join(0.3)