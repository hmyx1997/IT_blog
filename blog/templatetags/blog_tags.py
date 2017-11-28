# -*- coding: utf-8 -*-

from  ..models import Post,Category
from django import template

register = template.Library()

#获取数据库中最新的num篇文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]

#实现按月分归档
@register.simple_tag()
def archives():
    return Post.objects.dates('create_time','month',order='DESC')

#分类模板标签
@register.simple_tag()
def get_categories():
    return Category.objects.all()