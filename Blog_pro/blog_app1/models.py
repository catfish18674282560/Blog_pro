from django.db import models
from django.urls import reverse
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField                  # 导入富文本编辑器
from read_statistics.models import ReadNumCountExpansion, ReadDateNum        # 导入自定义阅读计数扩展类
from django.contrib.contenttypes.fields import GenericRelation               # 反向查询



class Blog_type(models.Model):
    # 类型
    type = models.CharField(verbose_name='分类', max_length=20)
    # 删除
    delete = models.BooleanField(default=True)

    def __str__ (self):
        return self.type

    class Meta():
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

class Blog(models.Model, ReadNumCountExpansion):                                # 继承自定义ReadNumCountExtension阅读计数扩展类
    title = models.CharField(verbose_name='标题', max_length=30, default='标题')
    # 内容
    content = RichTextUploadingField(config_name='ckeditor_all')
    # 设置用户外键
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户',  on_delete=models.CASCADE)
    # 类型外键
    blog_type = models.ForeignKey(Blog_type, verbose_name='分类', on_delete=models.CASCADE)       # 一对多关联，被关联对象通过.blog_set.all()属性方法，可以获取与之关联的QuerySet
    # 删除
    delete = models.BooleanField(default=True)
    # 反向查询
    generic_relation = GenericRelation(ReadDateNum)
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 最后修改时间
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    # 获取博客url
    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk':self.pk})
    
    # 获取用户
    def get_user(self):
        return self.author

    # 获取博客作者邮箱
    def get_email(self):
        return self.author.email
    
    def __str__(self):
        return '<Blog: %s>' % self.title
    
    # 该类为内部类，用于定义一些Django模型类的行为特性
    class Meta:
        # 指定QuerySet返回的结果集，按创建时间倒序排序(该类设置的排序会影响后台和前端)
        ordering = ['-creation_time']
        verbose_name = '博客'
        verbose_name_plural = verbose_name


