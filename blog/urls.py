# -*- coding: utf-8 -*-
"""IT_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),#输入基础网址进入首页
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),#从首页里获取某篇文章请求，通过正则表达式匹配并获取文章的pk
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    #通过正则取年月的值，传给views.py的archives函数
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    #通过正则取文章的pk，然后传参给views.py里的category函数
    url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag')
]
