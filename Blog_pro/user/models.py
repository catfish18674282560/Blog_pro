from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser             # 用户模型基类


# 保存第三方登陆关联关系
class OAuthRelationship(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='用户')
	# 记录openid的值
	appid = models.CharField(max_length=200,verbose_name='用户唯一ID')
	OAUTH_TYPE_CHOICES = (
		(0, 'QQ'),
		(1, '微信'),
		(2, '微博'),
	)
	# 设置第三方登陆关联有哪些
	oauth_type = models.PositiveIntegerField(default=0,choices=OAUTH_TYPE_CHOICES,verbose_name='第三方关联')
	# 保存图片地址
	portrait_img_url = models.URLField(null=True,verbose_name='图片地址')

	def __str__(self):
		return '<OAuthRelationship: %s>' % self.user.username

	class Meta():
		verbose_name = '第三方登陆关联'
		verbose_name_plural = verbose_name


# 继承用户模型基类，自定义用户模型
class MyUser(AbstractUser):
    nickName = models.CharField(max_length=10, default='', blank=True, verbose_name='昵称')               # 继承AbstractUser类，添加额外字段（注意：指定blank是为了后台修改昵称时允许表单提交空值）
    def __str__(self):
    	return self.nickName
    	
def get_nickName(self):                             # 自定义实例方法，返回昵称或用户名
    if self.nickName == '':                         # 判断当前用户有无昵称，没有昵称返回用户名，反之返回昵称
        return self.username
    return self.nickName

AbstractUser.get_nickName = get_nickName            # 向用户模型基类添加自定义方法
