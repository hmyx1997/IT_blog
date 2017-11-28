# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
# Create your views here.

def index(request):
    #以创建时间的降序生成文章列表
    post_list = Post.objects.all().order_by('-create_time')
    #渲染模板
    return render(request,'blog/index.html',context={'post_list':post_list})

#展示文章详细内容
def detail(request,pk):
    #会根据blog/urls.py中传过来的pk值来重定向至特定文章
    post = get_object_or_404(Post,pk=pk)
    #渲染模板
    return render(request,'blog/detail.html',context={'post':post})

