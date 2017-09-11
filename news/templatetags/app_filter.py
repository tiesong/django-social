"""
Implement custom Template tags
"""
from datetime import datetime
from django import template
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import re

register = template.Library()


@register.assignment_tag
def notifyUnread(username):
    """
    Return notification.
    :param user: 
    :return: 
    """

    def days_between(d1, d2):
        return abs((d2 - d1).days)

    notification_unread = []
    other_unread = []
    current_date = datetime.now()

    # Get unread Notification
    user = User.objects.filter(username=username).get()
    unread = user.notifications.unread()

    unread_exist = False
    other_exist = False
    # check exists if there is any event to perform after 24 hours.
    if len(unread) != 0:
        for item in unread:
            if days_between(item.target.start_date.replace(tzinfo=None), current_date.replace(tzinfo=None)) <= 1:
                unread_exist = True
                notification_unread.append(item)
            else:
                other_exist = True
                other_unread.append(item)

    return {"content": notification_unread,
            "other_content": other_unread,
            "count": len(notification_unread),
            "unread_exist": unread_exist,
            "other_exist": other_exist}


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


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


@register.filter(name="shortsnippet")
def shortsnippet(html_body):
    """
    Return snippet from html body
    :param html_body: 
    :return: 
    """
    snippet_txt = ""
    soup = BeautifulSoup(html_body, "html.parser")

    for p in soup.select("p"):
        snippet_txt += p.text

    return snippet_txt[:20]


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
