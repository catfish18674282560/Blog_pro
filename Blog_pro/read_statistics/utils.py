import datetime
from django.db.models import Sum
from django.utils import timezone   # 根据settings设置获取时间
from django.contrib.contenttypes.models import ContentType           # 导入ContentType模型类
from .models import ReadNum, ReadDateNum
from blog_app1.models import Blog



# 封装自定义计数
def read_statistics_count(request, obj):
   ct = ContentType.objects.get_for_model(obj)                       # 获取contenttype对象
   key = "%s_%s_read" % (ct.model, obj.pk)                           # 拼接Cookie键
   if not request.COOKIES.get(key):                                  # 判断cookie中有没有指定键
      # 通过.get_or_create()方法将查询不到的实例将根据查询条件创建，返回一个元组，元组中第一个参数为查询到或创建的实例，第二个参数为是否创建新的实例。
      readnum,create = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
      readnum.read_num += 1                                          # 阅读计数字段自增1
      readnum.save()                                                 # 保存进数据库

      today = timezone.now().date()
      read_date,create = ReadDateNum.objects.get_or_create(date=today, content_type=ct, object_id=obj.pk)
      read_date.read_num += 1
      read_date.save()

   return key                                                        # 返回拼接的Cookie键



# 今日热门博客
def hot_read_today():
   today = timezone.now().date()
   # 对筛选出来的博客按阅读量降序排序
   # 获取指定字段信息，保存在字典中返回QuerySet对象。
   hot_read_todays = Blog.objects.filter(generic_relation__date=today).order_by('-generic_relation__read_num') \
                                                                  .values('pk', 'title', 'generic_relation__read_num')
   return hot_read_todays[:9]



# 本周热门
def hot_read_week():
   today = timezone.now().date()
   this_week = today.isoweekday()
   last_sunday = today - datetime.timedelta(days=this_week)
   this_sunday = last_sunday + datetime.timedelta(days=7)
   # 筛选本月内访问过的所有博客
   # 通过.values()获取指定字段，保存在字典中返回
   # 先按Blog类pk、title字段进行分组，再通过.annotate(Sum())聚合函数统计。如果pk字段、title字段存在相同的那么它们的read_num字段的值将相加求和。（将指定字段重复的筛选掉）
   # 因为.annotate()方法会自动创建字段保存聚合结果，索引可以用read_sum字段进行降序排序
   hot_read_weeks = Blog.objects.filter(generic_relation__date__gt=last_sunday, generic_relation__date__lte=this_sunday) \
                                                                             .values('pk', 'title') \
                                                                             .annotate(read_sum=Sum('generic_relation__read_num')) \
                                                                             .order_by('-read_sum')
   return hot_read_weeks[:9]



# 本月热门
def hot_read_month():
   today = timezone.now().date()                                                    # 获取Django当前日期
   first_month = datetime.date(year=today.year, month=today.month, day=1)           # 拼接获取本月一号
   if today.month == 12:
      last_month = datetime.date(year=today.year+1, month=1, day=1)                 # 当月份为12时，获取下一年一月一号
   else:
      last_month = datetime.date(year=today.year, month=today.month+1, day=1)       # 获取下个月一号
   last_month = last_month - datetime.timedelta(days=1)                             # 下个月一号减一，获取本月月底

   # 筛选本月内热门博客，过滤掉重复博客并获取阅读量
   hot_read_months = Blog.objects.filter(generic_relation__date__gte=first_month, generic_relation__date__lte=last_month)\
                                                                           .values('pk', 'title') \
                                                                           .annotate(read_sum=Sum('generic_relation__read_num')) \
                                                                           .order_by('-read_sum')
   return hot_read_months[:9]
