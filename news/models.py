# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tinymce.models import HTMLField

from django.contrib.auth.models import User

from django.db import models


# Need to update settings.py to manage media files

class Category(models.Model):
    tag = models.CharField(max_length=150, default='General')

    def __str__(self):
        return self.tag


class News(models.Model):
    category = models.ManyToManyField(Category)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=150)
    article_text = models.TextField()

    article = HTMLField(blank=True)

    featured_image = models.ImageField(upload_to='news_images/%Y/%m/%d/', null=True, blank=True)
    image = models.ImageField(upload_to='news_images/%Y/%m/%d/', null=True, blank=True)

    pub_date = models.DateTimeField('date published')
    featured = models.BooleanField(default=False)

    feature_rank = models.IntegerField(default=0)


    def __str__(self):
    	return self.title

