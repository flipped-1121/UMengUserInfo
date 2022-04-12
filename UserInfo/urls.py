# -*- coding: utf-8 -*-
"""
   @Author: Kang
   @Version 1.0 
   @File: urls.py 
   @CreateTime: 2021/10/31 14:35
   @Software: PyCharm
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('login/', views.login),
    path('infoJson/', views.infoJson),
    path('show/', views.show),
]
