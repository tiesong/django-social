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