from django.shortcuts import render, redirect
from django.urls import reverse
from read_statistics.utils import hot_read_today, hot_read_week, hot_read_month
from django.core.cache import cache
from django.db.models import Q
from django.core.paginator import Paginator
from blog_app1.models import Blog

# 主页
def home(request):
    hot_read_months = cache.get('hot_read_months')              # 获取指定缓存数据
    if hot_read_months is None:                                 # 判断是否获取到指定缓存数据
        cache.set('hot_read_months', hot_read_month(), 3600)    # 将缓存数据以键值对保存在字典中，第三个参数为有效期（秒）
        print('正在缓存')
    else:
        print('已缓存')
    
    date = {}    
    date['hot_read_todays'] = hot_read_today()          # 今日热门
    date['hot_read_weeks'] = hot_read_week()            # 本周热门
    date['hot_read_months'] = hot_read_month()          # 本月热门
    return render(request, 'home.html', date)

# 特效粒子
def index(request):
    print(redirect(reverse('home')))
    context = {
        'my_blog_url': reverse('home'),             # 博客主页url
    } 
    return render(request, 'index.html', context)

# 站内搜索
def word_seaech(request):
    seaech = request.GET.get('word', '').strip()
    condition = None
    for i in seaech.split(' '):
        if condition is None:
            condition = Q(title__contains=i)
        else:
            condition = condition | Q(title__contains=i)
    blogs = Blog.objects.filter(condition)

    context = {}
    if not blogs:
        context['seaech'] = ''                  # 搜索内容
    else:
        context['seaech'] = seaech              # 搜索内容        

    paginator = Paginator(blogs, 10)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)

    context['paginator'] = paginator            # 分页器对象
    context['page'] = page
    context['page_list'] = page.object_list     # 当前页所有实例
    return render(request, 'word_seaech.html', context)