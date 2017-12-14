# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator
# Create your views here.

'''def index(request):
    #以创建时间的降序生成文章列表
    #post_list = Post.objects.all().order_by('-create_time')
    #渲染模板
    #return render(request,'blog/index.html',context={'post_list':post_list})'''

class IndexView(ListView):
        model = Post
        template_name = 'blog/index.html'
        context_object_name = 'post_list'
        paginate_by = 5

        def get_context_data(self, **kwargs):
            #获得父类生成传递给模板的字典
            context = super(IndexView,self).get_context_data(**kwargs)
            paginator = context.get('paginator')#Paginator的实例
            page = context.get('page_obj')#Page的实例
            is_paginated = context.get('is_paginated')#是否分页的bool

            #调用接下来自己写的分页函数
            pagination_data = self.pagination_data(paginator,page,is_paginated)

            #将分页导航条的模板变量更新至context
            context.update(pagination_data)

            return context

        def pagination_data(self,paginator,page,is_paginated):
            if not is_paginated:
                #如果不需要分页，也没有分页则返回空字典
                return {}
            left = []#当前页左边的页码，初始值为空

            right = []#当前页右边的页码，初始值为空

            left_has_more = False#第一页后面是否有省略号，初始值为无

            right_has_more = False#最后一页前是否有省略号，初始值为无

            first = False#是否需要显示第一页的号码，初始值为无

            last = False#是否显示最后一页的号码，初始值为无

            page_number = page.number#当前页页码

            total_pages = paginator.num_pages#分页后总页数

            page_range = paginator.page_range#分页页码列表

            if page_number == 1:#如果现在是第一页，获取页右边两个页码
                right = list(page_range)[page_number:page_number + 2]

                if right[-1]<total_pages -1:#如果最右边页码比最后一页-1还小，则有省略号
                    right_has_more=True

                if right[-1]<total_pages:#如果最右页码比最后一页小，则需要显示最后一页页码
                    last=True

            elif page_number==total_pages:#如果是最后一页，获取左边两页页码
                left=list(page_range)[(page_number-3)if(page_number-3)>0else 0:page_number-1]

                if left[0]>2:#最左的一页比第二页打，则需要省略号
                    left_has_more=True

                if left[0]>1:#最左一页比第一页大，则需要显示第一页
                    first=True

            else:#如果既不是最后也不是第一个，则获取左边右边的页码
                left=list(page_range)[(page_number-3)if(page_number-3)>0 else 0:page_number-1]
                right=list(page_range)[page_number:page_number+2]

                if right[-1]<total_pages-1:#如果最右边页码比最后一页-1还小，则有省略号
                    right_has_more=True
                if right[-1]<total_pages:#如果最右页码比最后一页小，则需要显示最后一页页码
                    last=True

                if left[0]>2:#最左的一页比第二页打，则需要省略号
                    left_has_more=True
                if left[0]>1:#最左一页比第一页大，则需要显示第一页
                    first=True

            data={
                'left':left,
                'right':right,
                'left_has_more':left_has_more,
                'right_has_more':right_has_more,
                'first':first,
                'last':last,
            }

            return data



#展示文章详细内容
def detail(request,pk):
    #会根据blog/urls.py中传过来的pk值来重定向至特定文章
    post = get_object_or_404(Post,pk=pk)
    #阅读数+1
    post.views_increase()
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

'''class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        #复写get，每一次文章被访问阅读数+1，必须返回HttpResponse
        #先调用父类的get才有self.object属性
        response = super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.views_increase()
        return response



    def get_context_data(self, **kwargs):
        #还要把评论表单和post下的评论列表传递给模板
        context =super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context'''

'''#按月份归档
def archives(request,year,month):
    #按月份年份过滤
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    #渲染模板
    return render(request, 'blog/index.html', context={'post_list': post_list})'''

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
                                                              create_time__month=month
                                                            ).order_by('-create_time')

    def get_context_data(self, **kwargs):
        # 获得父类生成传递给模板的字典
        context = super(ArchivesView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')  # Paginator的实例
        page = context.get('page_obj')  # Page的实例
        is_paginated = context.get('is_paginated')  # 是否分页的bool

        # 调用接下来自己写的分页函数
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新至context
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果不需要分页，也没有分页则返回空字典
            return {}
        left = []  # 当前页左边的页码，初始值为空

        right = []  # 当前页右边的页码，初始值为空

        left_has_more = False  # 第一页后面是否有省略号，初始值为无

        right_has_more = False  # 最后一页前是否有省略号，初始值为无

        first = False  # 是否需要显示第一页的号码，初始值为无

        last = False  # 是否显示最后一页的号码，初始值为无

        page_number = page.number  # 当前页页码

        total_pages = paginator.num_pages  # 分页后总页数

        page_range = paginator.page_range  # 分页页码列表

        if page_number == 1:  # 如果现在是第一页，获取页右边两个页码
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True

            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

        elif page_number == total_pages:  # 如果是最后一页，获取左边两页页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0else 0:page_number - 1]

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True

            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        else:  # 如果既不是最后也不是第一个，则获取左边右边的页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True
            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


'''#实现按分类归档
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    #按分类过滤
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    #渲染模板
    return render(request, 'blog/index.html', context={'post_list': post_list})'''

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        # 获得父类生成传递给模板的字典
        context = super(CategoryView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')  # Paginator的实例
        page = context.get('page_obj')  # Page的实例
        is_paginated = context.get('is_paginated')  # 是否分页的bool

        # 调用接下来自己写的分页函数
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新至context
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果不需要分页，也没有分页则返回空字典
            return {}
        left = []  # 当前页左边的页码，初始值为空

        right = []  # 当前页右边的页码，初始值为空

        left_has_more = False  # 第一页后面是否有省略号，初始值为无

        right_has_more = False  # 最后一页前是否有省略号，初始值为无

        first = False  # 是否需要显示第一页的号码，初始值为无

        last = False  # 是否显示最后一页的号码，初始值为无

        page_number = page.number  # 当前页页码

        total_pages = paginator.num_pages  # 分页后总页数

        page_range = paginator.page_range  # 分页页码列表

        if page_number == 1:  # 如果现在是第一页，获取页右边两个页码
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True

            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

        elif page_number == total_pages:  # 如果是最后一页，获取左边两页页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0else 0:page_number - 1]

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True

            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        else:  # 如果既不是最后也不是第一个，则获取左边右边的页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True
            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

    paginate_by = 5

    def get_context_data(self, **kwargs):
        # 获得父类生成传递给模板的字典
        context = super(TagView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')  # Paginator的实例
        page = context.get('page_obj')  # Page的实例
        is_paginated = context.get('is_paginated')  # 是否分页的bool

        # 调用接下来自己写的分页函数
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新至context
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果不需要分页，也没有分页则返回空字典
            return {}
        left = []  # 当前页左边的页码，初始值为空

        right = []  # 当前页右边的页码，初始值为空

        left_has_more = False  # 第一页后面是否有省略号，初始值为无

        right_has_more = False  # 最后一页前是否有省略号，初始值为无

        first = False  # 是否需要显示第一页的号码，初始值为无

        last = False  # 是否显示最后一页的号码，初始值为无

        page_number = page.number  # 当前页页码

        total_pages = paginator.num_pages  # 分页后总页数

        page_range = paginator.page_range  # 分页页码列表

        if page_number == 1:  # 如果现在是第一页，获取页右边两个页码
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True

            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

        elif page_number == total_pages:  # 如果是最后一页，获取左边两页页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0else 0:page_number - 1]

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True

            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        else:  # 如果既不是最后也不是第一个，则获取左边右边的页码
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = list(page_range)[page_number:page_number + 2]

            if right[-1] < total_pages - 1:  # 如果最右边页码比最后一页-1还小，则有省略号
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右页码比最后一页小，则需要显示最后一页页码
                last = True

            if left[0] > 2:  # 最左的一页比第二页打，则需要省略号
                left_has_more = True
            if left[0] > 1:  # 最左一页比第一页大，则需要显示第一页
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data



