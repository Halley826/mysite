#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/1/3 10:02 AM
# @Author : Halley@https://github.com/Halley826/
# @Version：V 1.0
# @File : urls.py
# @desc :映射，将html界面和函数一一对应
from django.urls import path
from . import views
app_name='usermng'
urlpatterns=[
    path('welcome',views.welcome,name='welcome'),
    path('index',views.index,name='index'),
    path('user_logout',views.index,name='user_logout'),
    path('register',views.register,name='register'),
    path('delete',views.delete,name='delete')
]
