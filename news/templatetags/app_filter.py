"""
Implement custom Template tags
"""
from django import template
from bs4 import BeautifulSoup
import re

register = template.Library()


@register.filter(name="snippet")
def snippet(html_body):
    """
    Return snippet from html body
    :param html_body: 
    :return: 
    """
    snippet_txt = ""
    soup = BeautifulSoup(html_body, "html.parser")

    for p in soup.select("p"):

        snippet_txt += p.text

    return snippet_txt[:150]


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

        snippet_txt += remove_img_tags(p.text)

    return snippet_txt


def remove_img_tags(data):
    p = re.compile(r'<img.*?/>')
    return p.sub('', data)


@register.filter(name="previewImage")
def previewImage(html_body):
    """
    Preview image from article.
    :param html_body: 
    :return: 
    """
    img_list = []

    soup = BeautifulSoup(html_body, "html.parser")

    for image in soup.select("img"):
        img_list.append(image)

    # Return Sample Image
    if len(img_list) == 0:
        return 'https://teamedup-ybf.s3.amazonaws.com/static/news/img/news-tmp.png'

    # Return base64 image.
    return img_list[0]["src"]
