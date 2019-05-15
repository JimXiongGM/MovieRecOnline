# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class UserProfile(AbstractUser):
    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    AGE_RANGE = (
        MaxValueValidator(150),
        MinValueValidator(1)
    )
    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default="")
    # 性别, 只能为男或女, 默认为男
    gender = models.CharField(max_length=7, verbose_name='性别', choices=GENDER_CHOICES, default='male')
    # 联系地址
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name='联系地址')
    # 年龄
    age = models.IntegerField(validators=AGE_RANGE, null=True, blank=True, verbose_name='年龄')
    # 头像 默认使用default.png
    image = models.ImageField(upload_to='image/%Y/%m', max_length=100, verbose_name='头像', default='image/default.png',
                              null=True, blank=True)
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(max_length=10, choices=(("register", "注册"), ("forget", "找回密码")),verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")  
    # datatime.now 需要将括号去掉, 如果不去掉的话会使用编译到这里时的时间, 只有将括号去掉的时候才会使用实例化时的时间

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100)  # image 在数据库中存储的是图片的路径地址
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="播放次序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "用户轮播图"
        verbose_name_plural = verbose_name
