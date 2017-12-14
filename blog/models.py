# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    #这是分类名类
    name = models.CharField(max_length=100)

    #这个函数可以让后台数据库取数据时显示更合理
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    #这是标签类
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    #这是文章类

    #文章标题
    title = models.CharField(max_length=70)

    #文章正文
    body = UEditorField('正文',height=300,width=1000,default=u'',
                        blank=True,imagePath='uploads/images/',toolbars='besttome',
                        filePath='uploads/files')

    #文章创建时间和最后修改时间
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章摘要，允许为空
    excerpt = models.CharField(max_length=200,blank=True)

    #分类与标签，分类是外码，一个分类下有许多文章是一对多的关系，一篇文章可以有
    #多个标签，一个标签下有多篇文章是多对多的关系
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    #文章作者，从django.contrib.auth.models导入User，一个作者会有多篇文章，一对多，外码
    author = models.ForeignKey(User)

    #文章阅读数
    views = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.title

    #每一次阅读文章都会阅读数+1
    def views_increase(self):
        self.views += 1
        self.save(update_fields=['views'])

    #每篇独立文章都会有独立的url，这个是用于重定向的函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})


