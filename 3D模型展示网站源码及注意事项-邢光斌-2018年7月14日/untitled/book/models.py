# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


#user功能表：进行表字段的设置
class UserProfile(AbstractUser):#登录用户信息存储
    nick_name = models.CharField(max_length=50,verbose_name=u"用户名",default="")
    birday = models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(max_length= 7,choices=(("male",u"男"),("female",u"女")),default="male")
    address = models.CharField(max_length=100,verbose_name=u"地址",default="")
    mobile = models.CharField(max_length=11,verbose_name=u"手机号",null=True,blank=True)
    # image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class ThereModels(models.Model):
    there_file = models.FileField(upload_to='media/mtl/%Y%m%d', max_length=100, default="")
    png_file = models.FileField(upload_to='media/mtl/%Y%m%d', max_length=100, default="",verbose_name=u"模型图片")
    up_time = models.DateTimeField(verbose_name="上传时间", default=datetime.now)
    model_name = models.CharField(max_length=50,verbose_name=u"模型名称", default="")
    download_times = models.IntegerField(default=0, verbose_name=u"下载次数")

    class Meta:
        verbose_name = "3D模型"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):#邮箱验证
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=20,verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name="验证码类型",choices=(("register","注册"),("forget","找回密码"),("update_email",u"修改邮箱")),max_length=30)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    #此处重载unicode方法，直接体现在页面显示上
    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)
    there_file = models.FileField(upload_to='media/%Y%m%d',max_length=100)


class ObjModels(models.Model):
    obj = models.ForeignKey(ThereModels,verbose_name=u"mtl文件")
    three_file = models.FileField(upload_to='media/obj/%Y%m%d', max_length=100, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    class Meta:
        verbose_name = u"obj文件"
        verbose_name_plural = verbose_name



class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name=u"接受用户")
    message = models.CharField(max_length=500,verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False,verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name;