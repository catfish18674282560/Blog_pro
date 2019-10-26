from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import OAuthRelationship


# 获取自定义用户模型对象
User = get_user_model()

# 用户登录
class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名',
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '请输入用户名或密码'
            }
        )
    )
    password = forms.CharField(
        label='密码',
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '请输入密码',
            }
        )
    )

    # 多个表单字段的验证
    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email','')
        password = self.cleaned_data.get('password','')
        user = authenticate(username=username_or_email, password=password)    # 从数据库验证用户名、密码，返回通过验证的user对象
        if username_or_email == '':
            raise forms.ValidationError('请输入用户名')

        if user is None:
            if User.objects.filter(email=username_or_email).exists():         # 判断是否存在该邮箱
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username,password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            else:
                raise forms.ValidationError('用户名或密码错误')                  # 未通过验证则触发指定错误
        else:
            self.cleaned_data['user'] = user                                   # 将通过验证的用户保存在cleaned_data字典中
        return self.cleaned_data                                               # 返回cleaned_data字典，保存了通过自定义验证的数据

# 注册用户
class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=20,
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '请输入（3-20位）用户名'
            }
        ),
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=20,
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '请输入（6-18位）密码',
            }
        ),
    )
    password_again = forms.CharField(
        label='重复输入密码',
        required=False,
        widget = forms.widgets.PasswordInput(
            attrs={
                'placeholder': '重复输入密码',
            }
        ),
    )
    email = forms.EmailField(
        label='邮箱',
        required=False,
        widget=forms.widgets.EmailInput(
            attrs={
                'class': 'get_email',
                'placeholder': '请输入邮箱',
            }
        ),
    )
    verification = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'verification_code'
            }
        ),
    )

    def __init__(self,*args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username','')
        if username == '':
            raise forms.ValidationError('请输入用户名')
        if User.objects.filter(username=username):                  # 数据库表User中查询用户名是否存在，判断用户有没有注册
            raise forms.ValidationError('该用户名已注册')
        return username                                             # 注意一定要返回验证完毕或修改的数据

    def clean_password_again(self):
        password = self.cleaned_data.get('password','')
        password_again = self.cleaned_data.get('password_again','')
        if password != password_again or password == '':
            raise forms.ValidationError('两次输入密码不匹配')
        return password_again

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        if email == '':
            raise forms.ValidationError('请输入邮箱')
        if User.objects.filter(email=email):
            raise forms.ValidationError('该邮箱已注册')
        return email

    def clean_verification(self):
        verification = self.cleaned_data.get('verification','')
        code = self.request.session.get('register_code','')         # 如果没有点“发送验证码”直接提交表单，会获取不到key所以这里要用.get()
        if verification == '' and code != verification:
            raise forms.ValidationError('验证码错误')
        return verification

# 修改昵称
class ChangeNickNameForm(forms.Form):
    changeNickname = forms.CharField(
        label="新昵称",
        max_length=15,
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder':'新昵称',                        # 表单中提示文字
            },
        ),
    )

    def __init__(self,*args,**kwargs):                        # 初始化方法，接收当前用户对象实参
        if 'user' in kwargs:
            self.user = kwargs.pop('user')                    # 删除并保存当前用户对象
        super().__init__(*args,**kwargs)

    def clean(self):
        user = self.user
        if not user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_changeNickname(self):
        nick_name = self.cleaned_data.get('changeNickname',None).strip()# 获取表单数据并去除前后空格
        if nick_name == '':
            raise forms.ValidationError('昵称不能为空')
        return nick_name                                        # 返回通过验证的表单数据


# 修改邮箱
class ChangeEmailForm(forms.Form):
    email = forms.EmailField(                              # 邮箱
        label='新邮箱',
        required=False,
        widget=forms.widgets.EmailInput(
            attrs={
                'class': 'get_email',
                'placeholder':'请输入新邮箱',
            },
        ),       
    )
    verification = forms.CharField(                             # 验证码
        label='验证码',
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'verification_code'
            }
        )
    )

    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args,**kwargs)
        
    def clean(self):
        user = self.request.user
        if not user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_email(self):                                          # 验证邮箱是否存在
        email = self.cleaned_data.get('email','').strip()
        if email == '':
            raise forms.ValidationError('请输入邮箱')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email

    def clean_verification(self):                                         # 验证验证码是否正确
        verification = self.cleaned_data.get('verification','')
        code = self.request.session.get('change_Email_code','')           # 如果没有点“发送验证码”直接提交表单，会获取不到key所以这里要用.get()
        if verification == '' and code != verification:
            raise forms.ValidationError('验证码错误')
        return verification

# 修改密码
class ChangePassword(forms.Form):
    old_password = forms.CharField(
        label='旧密码',
        strip=False,
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '旧密码'
            }
        )
    )
    new_password = forms.CharField(
        label='新密码',
        strip=False,
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '新密码'
            }
        )
    )
    again_password = forms.CharField(
        label='重复新密码',
        strip=False,
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '重复新密码'
            }
        )
    )
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password','')
        again_password = self.cleaned_data.get('again_password','')
        if new_password == '' or again_password != new_password:
            raise forms.ValidationError('两次输入密码不匹配')
        if not self.user.is_authenticated:
            raise forms.ValidationError('请登录')
        return self.cleaned_data
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password','')
        if not self.user.check_password(old_password):              # 验证密码对错
            raise forms.ValidationError('密码错误')
        return old_password

# 忘记密码
class ForgetPassword(forms.Form):
    new_password = forms.CharField(
        label='新密码',
        strip=False,
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '新密码'
            }
        )
    )
    again_password = forms.CharField(
        label='重复新密码',
        strip=False,
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '重复新密码'
            }
        )
    )
    email = forms.EmailField(
        label='邮箱',
        required=False,
        widget=forms.widgets.EmailInput(
            attrs={
                'class': 'get_email',
                'placeholder': '请输入绑定过的邮箱',
            }
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'verification_code'
            }
        )
    )
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args,**kwargs)

    def clean_again_password(self):
        new_password = self.cleaned_data.get('new_password','')
        again_password = self.cleaned_data.get('again_password','')
        if new_password == '' or again_password != new_password:
            raise forms.ValidationError('两次输入密码不匹配')
        return again_password

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        if not User.objects.filter(email=email).exists() or email == '':
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','')
        code = self.request.session.get('forget_Password_code','')              # 获取验证码类型
        if verification_code == '' or code != verification_code:
            raise forms.ValidationError('验证码错误')
        return verification_code

# 绑定QQ
class BindQQForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名',
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': '请输入用户名或密码'
            }
        )
    )
    password = forms.CharField(
        label='密码',
        required=False,
        widget=forms.widgets.PasswordInput(
            attrs={
                'placeholder': '请输入密码',
            }
        )
    )

    # 多个表单字段的验证
    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email','')
        password = self.cleaned_data.get('password','')
        user = authenticate(username=username_or_email, password=password)    # 从数据库验证用户名、密码，返回通过验证的user对象

        if username_or_email == '':
            raise forms.ValidationError('请输入用户名')

        if user is None:
            if User.objects.filter(email=username_or_email).exists():         # 判断是否存在该邮箱
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username,password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            else:
                raise forms.ValidationError('用户名或密码错误')                  # 未通过验证则触发指定错误
        else:
            self.cleaned_data['user'] = user                                    # 将通过验证的用户保存在cleaned_data字典中
        
        if OAuthRelationship.objects.filter(user=user, oauth_type=0).exists():  # 通过筛选OAuthRelationship模型的"user"和"oauth_type"两个字段来判断模型中是否存在该用户对象
            raise forms.ValidationError('该用户已绑定QQ')

        return self.cleaned_data
