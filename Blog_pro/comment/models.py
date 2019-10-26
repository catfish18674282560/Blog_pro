from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings

        

# 评论模块
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)    # 模型类
    object_id = models.PositiveIntegerField()                                  # 模型实例主键
    content_object = GenericForeignKey('content_type', 'object_id')            # 模型实例

    text = models.TextField()                                                  # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)                     # 评论时间
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)        # 评论用户

    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)           # 如果为None表示顶级评论，反之回复评论
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.CASCADE)       # 评论对象，也就是父级评论
    reply_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='replies', on_delete=models.CASCADE) # 回复用户
         
    def __str__(self):
        return self.text

    # 获取用户
    def get_user(self):
        return self.user

    # 获取评论模型的URL
    def get_url(self):
        return self.content_object.get_url()

    class Meta():
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering =  ['comment_time']           # 按评论时间顺序排序
