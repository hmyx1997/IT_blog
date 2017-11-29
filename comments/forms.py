# -*- coding: utf-8 -*-

from django import forms #django的表单功能
from .models import Comment

class CommentForm(forms.ModelForm):
    #内部类
    class Meta:
        model = Comment
        fields = ['name','email','url','text']#指定需要显示的字段