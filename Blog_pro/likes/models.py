from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings


# 记录模型实例点赞数量
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    like_num = models.IntegerField(default=0)       							# 点赞数量
    
    def __str__(self):
        return '<LikeCount: %s>' % self.like_num

    class Meta():
        verbose_name = '博客点赞总数'
        verbose_name_plural = '博客点赞总数'
   

# 记录已经点赞的用户
class LikeRecord(models.Model):
   content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
   object_id = models.PositiveIntegerField()
   content_object = GenericForeignKey('content_type', 'object_id')

   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)          # 点赞用户
   like_time = models.DateTimeField(auto_now_add=True)               					 # 点赞时间
   
   def __str__(self):
        return '<LikeRecord: 用户:%s 时间:%s>' % (self.user.username, self.like_time)

   class Meta():
        verbose_name = '已点赞的用户'
        verbose_name_plural = '已点赞的用户'


