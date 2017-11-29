# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from blog.models import Post

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)#评论用户名
    email = models.CharField(max_length=255)#评论用户邮箱
    url = models.URLField(blank=True)#评论用户个人网站
    text = models.TextField()#正文
    create_time = models.DateTimeField(auto_now_add=True)#评论时间，自动取评论发生时间

    #一篇博文可以有多个评论
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return self.text[:20]
