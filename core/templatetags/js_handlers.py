# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse_lazy


register = template.Library()


@register.filter(name='go_to_url')
def go_to_url(url):
    """ snippet extracted from https://gist.github.com/srstanic/3059893 """
    url_ = reverse_lazy(url)
    return "window.location='" + url_ + "'; return false;"
