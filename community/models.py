# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth.models import User
from bs4 import BeautifulSoup


class Category(models.Model):
    tag = models.CharField(max_length=150, default='Industry')
    
    def __str__(self):
        return self.tag


class Company(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    admin = models.ManyToManyField(User, blank=True)
    description = HTMLField(blank=True)
    partner = models.BooleanField(default=False)
    size = models.IntegerField(null=True)

    image = models.ImageField(upload_to='company_images/%Y/%m/%d/', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    
    website = models.CharField(max_length=155, blank=True, null=True)
    twitter = models.CharField(max_length=155, blank=True, null=True)
    facebook = models.CharField(max_length=155, blank=True, null=True)
    linkedin = models.CharField(max_length=155, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def _get_portal_image(self):
        "Returns the company's portal image."
        try:
            img_list = []
            soup = BeautifulSoup(self.description, "html.parser")
            
            for image in soup.select("img"):
                img_list.append(image)
            
            # Return Sample Image
            if len(img_list) == 0:
                return 'https://teamedup-ybf.s3.amazonaws.com/static/news/img/news-tmp.png'
            
            # Return base64 image.
            return img_list[0]["src"]
        except Exception as e:
            print('Error: {}'.format(e))
            return 'https://teamedup-ybf.s3.amazonaws.com/static/news/img/news-tmp.png'
    
    portal_image = property(_get_portal_image)


class Tag(models.Model):
    tag = models.CharField(max_length=150)
    
    def __str__(self):
        return self.tag


# Need to update settings.py to manage media file s
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tagline = models.CharField(max_length=155, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    advisor = models.BooleanField(default=False)
    
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', null=True, blank=True)
    
    phone_number = models.CharField(max_length=30, blank=True, null=True, default=None)
    
    website = models.CharField(max_length=155, blank=True, null=True)
    twitter = models.CharField(max_length=155, blank=True, null=True)
    facebook = models.CharField(max_length=155, blank=True, null=True)
    linkedin = models.CharField(max_length=155, blank=True, null=True)
    
    bio = HTMLField(blank=True)
    
    companies = models.ManyToManyField(Company, blank=True)
    
    def __str__(self):
        return self.user.username
