from django.contrib import admin
from .models import Blog_type, Blog                        # 按编辑模型类的顺序导入，并自定义其模型管理界面


# 注册Blog_type模型类
@admin.register(Blog_type)
class Blog_typeAdmin(admin.ModelAdmin):
    # 后台要显示的模型字段
    list_display = ('pk', 'type')
    list_filter = ('delete',)


@admin.register(Blog)
class Blog(admin.ModelAdmin):
    # 后台要显示的模型字段
    list_display = ('pk', 'title', 'author', 'blog_type', 'get_read_num', 'creation_time', 'modify_time', 'delete')   # get_read_num该字段是继承ReadNumCountExpansion扩展类
    list_per_page = 30

    def get_read_num(self, obj):                    # 重写自定义获取阅读总数的方法，obj指向当前类的实例
        return obj.get_read_num()                   # 指定返回值
    get_read_num.short_description = '阅读人数'      # 自定义"get_read_num"方法在admin列表中显示的列名
