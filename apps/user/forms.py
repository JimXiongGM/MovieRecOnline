#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: forms.py 
@time: 18-6-21 上午12:45 
"""
from django import forms


class LoginForm(forms.Form):
    # requried=True 如果表单中这个值不能为空
    # username 和password的变量名要和request.POST中(也就是html中form中的name名字一致)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
