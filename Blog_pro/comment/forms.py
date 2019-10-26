from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from .models import Comment



class CommentForm(forms.Form):
   content_type = forms.CharField(                             # 保存的评论的模型类
      widget=forms.widgets.HiddenInput()                       # 注意下面HiddenInput都需要设置初始值
   )
   object_id = forms.IntegerField(                             # 保存的评论模型类实例主键
      widget=forms.widgets.HiddenInput()
   )
   text = forms.CharField(
      widget=forms.widgets.Textarea()
   )
   reply_comment_id = forms.IntegerField(                      # 保存顶级评论的id
      widget=forms.widgets.HiddenInput(
         attrs={'id': 'reply_comment_id'}
      ),
   )

   def __init__(self, *args, **kwargs):                        # 接收该类传入的实参
      if 'user' in kwargs:                                     # 判断user在不在kwargs字典中
         self.user = kwargs.pop('user')                        # 删除kwargs字典中指定元素，并保存在self.user属性里
      super().__init__(*args, **kwargs)                        # 调用父类初始化方法

   def clean(self):
      if self.user.is_authenticated:                           # 判断用户是否登录
         self.cleaned_data['user'] = self.user                 # 用户登录时，向cleaned_data字典中保存当前用户
      else:
         raise forms.ValidationError('用户尚未登录')            # 用户未登录时，提示异常信息

      content_type = self.cleaned_data['content_type']                                 # 获取表单字段提交的模型类名
      object_id = self.cleaned_data['object_id']                                       # 获取表单字段提交的模型实例pk
      try:
         model_class = ContentType.objects.get(model=content_type).model_class()       # 筛选ContentType里指定model字段实例，再获取该实例的模型类对象
         model_obj = model_class.objects.get(pk=object_id)                             # 通过主键筛选模型类实例对象
         self.cleaned_data['content_object'] = model_obj                               # 将模型类实例对象保存进cleaned_data字典中
      except exceptions.ObjectDoesNotExist:                       
         raise forms.ValidationError('评论对象不存在')
      
      if not self.cleaned_data['text']:
         raise forms.ValidationError('评论内容不能为空！')
      return self.cleaned_data

   # 验证评论对象
   def clean_reply_comment_id(self):
      reply_comment_id = self.cleaned_data['reply_comment_id']
      if reply_comment_id < 0:
         raise forms.ValidationError('回复对象不存在')
      elif reply_comment_id == 0:                                                
         self.cleaned_data['parent'] = None                                      # 如果等于0，则说明是创建顶级评论
      elif Comment.objects.filter(pk=reply_comment_id):                          # 判断是否是某评论对象的主键
         self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)  # 将该评论对象保存返回
      else:
         raise forms.ValidationError('回复对象不存在')
      return reply_comment_id
