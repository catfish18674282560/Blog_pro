from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings                            # 导入settings.py全局设置文件
from django.db.models import Count
from read_statistics.utils import read_statistics_count     # 导入自定义封装阅读计数扩展函数
from .models import Blog, Blog_type


# 公共分页器函数
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.PAGINATOR_PAGE_NUMBER)                       # 调用分页器，将需要进行分页的QuerySet，和每页多少博客数量传入
    page_num = request.GET.get('page', 1)                                                       # 从GET请求中获取页码对象
    pages = paginator.get_page(page_num)                                                        # 获取页码.get_page()方法会自动转换为int类型
    current_page = pages.number                                                                 # 获取当前页码
    # 逻辑：列表推导式，通过获取‘当前页码数’前后两个页码数，然后显示在前端，从而达到页码数缩短。
    # 通过range()函数求出‘当前页码’前面两个页码数，
    # 起始页码数索引：因为页码不能为零或负数，又因为起始页码数最小必须是1，所以max()函数获取‘当前页码数’-2的值与1作比较取最大值。
    # 结束页码数索引：当前页码。
    # 通过range()函数求‘当前页码数’后面两个页码数，
    # 起始页码数索引：当前页码。
    # 结束页码数索引：因为‘结束页码数’不能超过总页码数，所以这里通过min()函数让‘当前页码数’后面第二个页码数与总页码数作比较取最小值。又因为是结束索引，所以要+1
    page_range = list(range(max(current_page-2, 1), current_page)) + \
                 list(range(current_page, min(current_page+2, paginator.num_pages)+1))

    # 逻辑：如果'当前页码'前面第二个页码数，不能与'起始页码数'顺序拼接时，那么该页码数就是判断参数3.
    #        page_range[0]表示当前页码前面第二个页码数，起始页码数为1
    if page_range[0] >= 3:
        page_range.insert(0, "...")
    # 逻辑：如果'当前页码'后面第二个页码数，不能与'总页码数'顺序拼接时，那么该页码数就是判断参数（该参数通过总页码数-当前页码后面第二个页码数获得）。
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")

    # 逻辑：如果'当前页码'前面第二个页码数不是1时，那么就说明‘当前页码数前面第二个页码数’与‘起始页码数’之间相差最少一个数，那么就可以在‘页码列表’第一个位置添加1.
    if page_range[0] != 1:
        page_range.insert(0, 1)
    # 逻辑：如果‘当前页码数’后面第二个页码数不是‘总页码数时’，那么就说明‘当前页码数后面第二个页码数’与‘总页码数’之间相差最少一个数，那么就可以在‘页码列表’最后一个位置添加‘总页码数’
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    data = {}
    data['blogs'] = blogs_all_list                                                                              # QuerySet
    data['Blogs'] = pages.object_list                                                                           # 获取当前这一页所有博客并保存在列表中返回，再添加进字典
    data['pages'] = pages                                                                                       # 获取的页码
    data['page_range'] = page_range                                                                             # 当前页码数及前后两个页码数组成的列表
    return data                                                                                                 # 返回字典对象



# 博客主页
def blog_home(request):
    blogs_all_list = Blog.objects.filter(delete=True)                                                                   # 获取所有符合条件的Model对象，返回QuerySet

    # 年月日统计写法
    blog_dates = Blog.objects.dates('creation_time', 'day', order='DESC')                                               # 获取不重复的年月日对象，并保存在列表中
    blog_date_dic = {}
    for blog_date in blog_dates:                                                                                        # 对获取到的不重复年月日对象，进行遍历
        blog_date_count = Blog.objects.filter(creation_time__year=blog_date.year,                                       # 遍历每执行一次，就筛选出所有指定的年份、月份、日份的Model对象，返回QuerySet，再通过.count()获取它的的长度
                            creation_time__month=blog_date.month, creation_time__day=blog_date.day).count()
        blog_date_dic[blog_date] = blog_date_count                                                                      # 遍历每执行一次，就将遍历到的当前datetime.date对象作为Key，筛选出的指定年月日QuerySet长度作为Value，保存在字典变量中

    data = get_blog_list_common_data(request, blogs_all_list)                                                           # 调用自定义分页器函数
    data['blog_dates'] = blog_date_dic                                                                                  # 保存不重复年月日datetime.date对象，以及其Model对象个数
    data['types'] = Blog_type.objects.annotate(blog_count=Count('blog'))                                                # 计算每个博客类型里的博客数量
    return render(request, 'blog_home.html', data)


# 类型分类
def blog_type(request, blog_type_pk):
    blog_type = Blog_type.objects.get(pk=blog_type_pk)                                                      # 获取Blog_type模型类中主键为blog_type_pk的Model对象
    blog_types = Blog.objects.filter(blog_type=blog_type, delete=True)                                      # 获取Blog模型类中blog_type字段的值为blog_type的所有Model对象，返回QuerySet

    data = {}
    data['blog_type'] = blog_type
    data = get_blog_list_common_data(request, blog_types)
    return render(request, 'blog_type_pk.html', data)


# 时间分类
def blog_date(request, year, month, day):
    blog_dates = Blog.objects.filter(creation_time__year=year, creation_time__month=month, creation_time__day=day, delete=True)         # 获取满足指定日期的所有Model对象，返回QuerySet
    data = get_blog_list_common_data(request, blog_dates)                                                                               # 调用自定义分页器

    data['blog_year_month_day'] = "%s年%s月%s日" % (year, month, day)
    data['blog_dates'] = Blog.objects.dates('creation_time', 'day', order='DESC')
    return render(request, 'blog_date.html', data)


# 详情
def blog_detail(request, blog_pk):
    blog = Blog.objects.get(pk=blog_pk, delete=True)                                   # 获取Blog模型类中主键为blog_pk，的model对象
    cookie_key = read_statistics_count(request, blog)                                  # 调用自定义封装阅读计数函数

    data = {}
    data['Blog'] = blog
    data['previous_page'] = Blog.objects.filter(creation_time__lt=blog.creation_time).first()
    data['next_page'] = Blog.objects.filter(creation_time__gt=blog.creation_time).last()

    response = render(request, 'blog_detail.html', data)                                # 获取响应（服务器发送回来的）
    response.set_cookie(cookie_key, 'true', max_age=3600)                                 # 为当前Model对象定义cookie，并设置有效期10秒（cookie是一个字典类型）
    return response
