from .forms import LoginForm


# 自定义向模板标签中添加默认变量，LoginForm在模板中可以直接使用。
def login_form(request):                   # 注意：request形参必须写
    return {'LoginForm': LoginForm()}