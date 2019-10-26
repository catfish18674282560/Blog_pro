from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from blog_app1.models import Blog
from ..forms import CommentForm


register = template.Library()
# 获取博客评论数量
@register.simple_tag()
def get_blog_comment(obj):
    ct = ContentType.objects.get_for_model(Blog)
    return Comment.objects.filter(content_type=ct, object_id=obj.pk).count()


# 评论表单控件
@register.simple_tag()
def form_comment(obj):
    blog_ct = ContentType.objects.get_for_model(Blog)      # 获取Blog模型类的ContentType实例

    comment_data = {}
    comment_data['content_type'] = blog_ct.model           # 初始化模型类，注意：必须通过.model获取字符串类型
    comment_data['object_id'] = obj.pk                     # 初始化当前博客pk
    comment_data['reply_comment_id'] = 0                   # 初始化回复的评论对象id值（该值为0时，说明是评论。如果是非0就是评论对象的id）
    return CommentForm(initial=comment_data)               # 设置评论表单初始值（实现保存当前评论的模型名，模型实例的pk）


# 评论列表
@register.simple_tag()
def get_comment(obj):
    ct = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None).order_by('-comment_time')     # 筛选所有顶级评论，并按创建时间倒序排序


