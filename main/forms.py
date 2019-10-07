from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import User

class loginForm(forms.Form):
    # 原本继承自forms.ModelForm, User模型里的email要求唯一,
    # class Meta:
    #     model = User
    #     fields = ['email', 'password']
    # 这样生成的form要求输入的email唯一, 与已注册用户矛盾, 因此还是得使用forms.Form
    email = forms.EmailField()
    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput
        )

class registerForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(required=True)
    confirm_email = forms.EmailField(required=True)
    password = forms.CharField(
        # 要求密码不多于16位
        max_length=16,
        # 要求密码不少于8位, 并且至少包含一个数字,一个大写字母,一个小写字母
        # validator的用法来自 https://docs.djangoproject.com/en/2.2/ref/validators/
        # 正则表达式的写法来自
        # https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
        validators=[RegexValidator("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", "密码格式有误.")],
        # 必须添加如下widget, 不然密码会明文显示
        widget=forms.PasswordInput,
        required=True,
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        # 本来我用的是User.objects.get()但是会报错, 因为如果数据不存在, get会raise DoesNotExist异常
        # 与其多加一句except, 不如直接使用filter().exists()
        # 文档参见 https://docs.djangoproject.com/en/2.2/ref/models/querysets/#queryset-api
        if User.objects.filter(username=username).exists():
            # self这里raise的ValidationError都会统一添加进form.errors
            # 然后在template文件中以<ul>中的元素呈现
            # 文档参见 https://docs.djangoproject.com/en/2.2/ref/forms/api/#how-errors-are-displayed
            raise forms.ValidationError(
                _("Username already taken %(name)s"),
                code="not unique",
                params={'name':username},
            )
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # 如果使用User.objects.get()会产生 DoesNotExist 异常, 因此使用filter
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _("Email already taken %(email)s"),
                code="email must be unique",
                params={'email':email}
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email and confirm_email: # 避免两个都是None
            if email != confirm_email:
                raise forms.ValidationError(
                    _("Email not consistent"),
                    code = "invalid email"
                )

# clean() 和 clean_<fieldname>()函数的用法可以参考文档:
# https://docs.djangoproject.com/en/2.2/ref/forms/validation/
# 完整的validator写法 参见 https://docs.djangoproject.com/en/2.2/ref/validators/
# 使用了 django.utils.translation 里的 gettext_lazy