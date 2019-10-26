from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _              # 翻译类
from .models import OAuthRelationship


User = get_user_model()                    # 获取自定义的用户模型类对象
@admin.register(User)                      # 注册自定义的用户模型类对象
class UserAdmin(BaseUserAdmin):            # 继承UserAdmin，会使用默认设置的后台显示字段排序
    fieldsets = (			               # 重写默认后台管理界面（可以直接使用自定义用户类中的所有字段）
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickName', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'nickName', 'email', 'is_staff', 'is_active', 'is_superuser')           # 用户名、昵称、邮箱、是否为管理员、是否激活、是否为超级用户

# 第三方登陆关联
@admin.register(OAuthRelationship)
class OAuthRelationshipAdmin(admin.ModelAdmin):
	fields = ('user', 'appid', 'oauth_type', 'portrait_img_url')