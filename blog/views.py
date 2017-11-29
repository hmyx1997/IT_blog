# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
import markdown
from comments.forms import CommentForm
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
    #这是这个CommentForm类的实例化
    form = CommentForm()
    #获取文章下的所有评论
    comment_list = post.comment_set.all()
    #将文章，表单，评论作为模板变量传给模板
    context = {'post': post,
               'form': form,
               'comment_list': comment_list}
    # 渲染模板
    return render(request, 'blog/detail.html', context=context)

#按月份归档
def archives(request,year,month):
    #按月份年份过滤
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    #渲染模板
    return render(request, 'blog/index.html', context={'post_list': post_list})

#实现按分类归档
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    #按分类过滤
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    #渲染模板
    return render(request, 'blog/index.html', context={'post_list': post_list})



