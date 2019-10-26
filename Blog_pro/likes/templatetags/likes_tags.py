from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()
@register.simple_tag
def get_like_count(obj):                             # obj形参接收当前被点赞实例对象
    ct = ContentType.objects.get_for_model(obj)
    like_count, create = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.pk)     # 获取/创建当前被点赞对象的LikeCount模型实例。
    return like_count.like_num                       # 获取当前被点赞对象的点赞总数


@register.simple_tag(takes_context=True)             # 获取当前模板的context字典对象
def add_like(context, obj):                          # context该形参中保存了当前模板中所有变量。（注意：context必须写在第一个形参）
    ct = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''                                    # 如果用户未登录，则返回空字符串，显示未点赞状态，下面代码不执行

    if LikeRecord.objects.filter(content_type=ct, object_id=obj.pk, user=user).exists(): # 判断LikeRecord模型中有无指定条件实例对象
        return 'like_img2'                           # 如果存在指定实例对象，显示已点赞状态
    else:
        return ''                                    # 反之表示当前用户未点过赞，返回空字符串，显示未点赞状态


@register.simple_tag
def get_content_type(obj):
    # 注意：索然该函数返回的是字符串，但是在模板中会被认为变量！
    return ContentType.objects.get_for_model(obj).model   # 动态获取传入的模型/实例对象的ContentType类型，再获取其模型类名小写