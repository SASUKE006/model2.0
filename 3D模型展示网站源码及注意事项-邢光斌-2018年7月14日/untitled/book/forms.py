# _*_ coding: utf-8 _*_
__auther__ = '刘凌晨'
__date__ = '2018/3/28 8:27'

from django import forms
from captcha.fields import CaptchaField


from .models import UserProfile

#登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=20)#表示为必填字段
    password = forms.CharField(required=True,min_length=5,max_length=15)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


