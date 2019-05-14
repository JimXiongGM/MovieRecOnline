#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: urls.py 
@time: 18-6-21 上午12:46 
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('user', TemplateView.as_view(template_name="index.html"), name="index"),
]
