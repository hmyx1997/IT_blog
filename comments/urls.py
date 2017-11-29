# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment'),
    #通过正则匹配url并取post_pk的值，传参并调用post_comment函数
]