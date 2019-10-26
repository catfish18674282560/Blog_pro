from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord


# 封装错误信息
def ErrorResponse(status,error):
    data = {}
    data['status'] = status
    data['error'] = error                   # 错误信息描述
    return JsonResponse(data)

# 封装需要返回的JSON数据
def SuccessResponse(status,like_count):
    data = {}
    data['status'] = status              # 返回数据成功
    data['like_count'] = like_count           # 总点赞数
    return JsonResponse(data)

# 处理ajax请求数据
def like_change(request):
    user = request.user                         # 获取当前用户对象
    if not user.is_authenticated:               # 判断用户是否登陆
        return ErrorResponse('001', '请登录后点赞')

    content_type = request.GET['content_type']  # 动态获取点赞模型对象字符串，因为GET获取的数据都是字符串
    object_id = int(request.GET['object_id'])   # 动态获取点赞对象实例。因为通过GET获取的都是字符串，所以这里需要进行int()转换

    # 捕获查询异常
    try:
        content_type = ContentType.objects.get(model=content_type)     # 获取ContentType实例
        model_class = content_type.model_class()                       # 获取该ContentType实例所对应的模型类对象
        model_obj = model_class.objects.get(pk=object_id)              # 获取该模型类对象中指定pk实例
    except exceptions.ObjectDoesNotExist:
        return ErrorResponse('500','获取不到点赞对象')

    
    # 通过创建当前用户的LikeRecord模型实例，来记录该用户是否已经点过赞。
    # 当进行点赞操作时，如果LikeRecord模型中存在当前用户实例，则创建当前点赞对象的LikeCount模型实例，并且like_num字段自增。
    if request.GET['is_like'] == 'true':                            # 如果为true表示未点赞状态，false表示已点赞状态
        # 获取/创建当前用户的LikeRecord模型实例。
        like_record, create = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        # 如果是新创建的，则说明当前用户未点赞。获取当前点赞对象LikeCont模型实例，like_num字段自增。
        if create:
            like_count,create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse('200',like_count.like_num)
        
        # 如果直接获取了，则说明当前用户已点赞
        else:
            return ErrorResponse('500','您已经点赞过，不能重复点赞')
        
    # 当进行取消点赞操作时，通过判断当前用户的LikeRecord模型实例，如果存在则当前点赞对象的LikeCount模型实例的like_num字段自减。
    else:
        # 如果LikeRecord模型中存在当前用户实例，则说明当前用户已点赞。
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 如果LikeRecord模型中存在当前用户实例，则说明该用户已经点过赞。取消点赞就需要删除该实例
            LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user).delete()
            # 获取/创建当前点赞对象的LikeCount模型实例。
            like_count,create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not create:
                # 当前点赞对象的Like_Count模型实例like_num字段自减
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse('200',like_count.like_num)
            else:
                # 如果是新创建对象，则说明该点赞对象没有LikeCount模型实例，数据错误
                return ErrorResponse('500','数据错误，无法取消点赞')
            
        # 如果LikeRecord模型中没有当前用户实例，则说明当前用户为进行过点赞
        else:
            return ErrorResponse('500','您未点赞过，无法取消点赞')
