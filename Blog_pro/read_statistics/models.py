from django.db import models
from django.utils import timezone
from django.db.models.fields import exceptions                                  # 导入异常模块
from django.contrib.contenttypes.models import ContentType                      # 导入ContentType模型类（该类包括当前项目app内所有模型类）
from django.contrib.contenttypes.fields import GenericForeignKey


# 总阅读统计
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)      # 设置ContentType一对多关联
    object_id = models.PositiveIntegerField()                                       # 该对象保存Model对象pk
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return '<ReadNum: %s>' % self.read_num

    class Meta():
        verbose_name = '博客访问数量'
        verbose_name_plural = verbose_name


# 获取每一篇博客的阅读数（Blog的扩展类）
class ReadNumCountExpansion():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)                               # 获取ContentType实例对象
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)          # 获取ReadNum模型类中满足条件的实例对象
            return readnum.read_num                                                    # 返回当前实例的阅读数
        except exceptions.ObjectDoesNotExist:                                          # 因为没有访问过的博客获取不到readnum属性，所以获取不到该属性值。
            return 0                                                                   # 如果未被访问过的博客访问量显示0，就需要返会0


# 日期阅读统计
class ReadDateNum(models.Model):
    date = models.DateField(default=timezone.now().date())
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '<ReadDateNum: 日期:%s 数量:%s>' % (self.date, self.read_num)

    class Meta():
        verbose_name = '日期阅读统计'
        verbose_name_plural = verbose_name

