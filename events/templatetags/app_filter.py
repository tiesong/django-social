"""
Implement custom Template tags
"""
from django import template
from bs4 import BeautifulSoup
import re

register = template.Library()


@register.filter(name="fulltext")
def fulltext(html_body):
    """
    Return snippet from html body
    :param html_body: 
    :return: 
    """
    snippet_txt = ""
    soup = BeautifulSoup(html_body, "html.parser")

    for p in soup.select("p"):

        snippet_txt += p.text

    return snippet_txt


@register.filter(name="previewImage")
def previewImage(html_body):
    """
    Preview image from article.
    :param html_body: 
    :return: 
    """
    img_list = []
    soup = BeautifulSoup(html_body, "html.parser")
    print('select: {}'.format(soup.select("img.src")))

    for image in soup.select("img"):
        img_list.append(image)

    # Return Sample Image
    if len(img_list) == 0:
        return '../static/news/img/news-tmp.png'

    # Return base64 image.
    return img_list[0]["src"]
