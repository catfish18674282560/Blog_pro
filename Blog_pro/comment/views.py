from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


# 获取前端表单字段提交内容
def update_comment(request):
    data = {}
    comment_form = CommentForm(request.POST, user=request.user)                # 向表单类传入关键字参数
    if comment_form.is_valid():
        # 创建顶级评论
        comment = Comment()
        comment.text = comment_form.cleaned_data['text']                        # 新创建评论内容
        comment.user = comment_form.cleaned_data['user']                        # 新创建评论用户
        comment.content_object = comment_form.cleaned_data['content_object']    # 新创建评论模型类实例对象

        # 创建parent对象的回复评论
        parent = comment_form.cleaned_data['parent']                             # None表示评论，反之表示回复评论
        if parent:                                                               # 判断不是顶级评论时
            comment.root = parent.root if not parent.root is None else parent    # 顶级评论
            comment.parent = parent                                              # 回复的评论，也就是父级评论
            comment.reply_to = parent.user                                       # 回复谁
        comment.save()
      
        # 服务器返回到前端Ajax数据
        data['status'] = "SUCCESS"                                             # 服务器响应数据获取成功
        data['username'] = comment.user.get_nickName()                         # 将新创建的评论对象用户名或昵称发送到前端(".get_nickName()"自定义获取用户名/昵称方法)
        data['comment_time'] = comment.comment_time.timestamp()                # 将评论时间转换为时间戳（带时区的）
        data['text'] = comment.text                                            # 新创建的评论内容
        data['content_type'] = ContentType.objects.get_for_model(comment).model# 模型类字符串

        if not parent is None:                                                 # 判断是否是回复评论
            data['reply_to'] = comment.reply_to.get_nickName()                  # 返回回复用户对象的用户名/昵称(".get_nickName()"自定义获取用户名/昵称方法)
        else:
            data['reply_to'] = ''                                               # 如果是顶级评论返回空
        data['pk'] = comment.pk                                                # 返回评论对象主键（可能是顶级评论、回复评论）
        data['root_pk'] = comment.root.pk if not comment.root is None else ''  # 返回回复评论对象的爷爷级评论对象的主键
    else:
        data['status'] = "ERROR"                                               # 服务器响应数据获取失败
        data['message'] = list(comment_form.errors.values())[0][0]             # 取出表单错误转换成列表后里面的错误信息
    return JsonResponse(data)                                                 # 转换为JSON数据格式并返回

