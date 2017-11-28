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
    url(r'^$',views.index,name='index'),#输入基础网址进入首页
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),#从首页里获取某篇文章请求，通过正则表达式匹配并获取文章的pk

]
