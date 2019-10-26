from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog_home, name='blog_home'),                                        # 博客主页
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),                       # 博客详情
    path('type/<int:blog_type_pk>', views.blog_type, name='blog_type'),                 # 博客所有美型，因为前面是一个数字类型，这个也是数字类型，python会认为是一个值，所以需要前面隔开
    path('date/<int:year>/<int:month>/<int:day>', views.blog_date, name='blog_date'),   # 当前博客日期
]
