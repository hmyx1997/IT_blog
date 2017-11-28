# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post,Category,Tag
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)