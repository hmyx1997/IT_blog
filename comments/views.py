# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):
    #获取被评论的文章，然后把这篇文章和后面的评论关联起来
    post = get_object_or_404(Post,pk=post_pk)

    #当有POST请求时才处理评论表单数据
    if request.method == 'POST':
        #request.POST是一个类字典对象，评论在这里面，然后生成一个CommentForm实例
        form =CommentForm(request.POST)

        #验证评论数据是否合法
        if form.is_valid():
            #先生成一个Comment实例
            comment = form.save(commit=False)

            #将评论和文章关联起来
            comment.post = post

            #将评论存进数据库
            comment.save()

            #重定向至post的详情页的url，通过get_absolute_url函数
            return redirect(post)

        else:
            #如果评论内容不合法则获取原有所有评论，用这些评论，和文章去渲染模板
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list}
            return render(request,'blog/detail.html',context=context)

        #无POST请求则没有提交评论，重定向至文章详情页
        return  redirect(post)

