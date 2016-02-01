# -*- coding: utf-8 -*-

from ..money import money_format as mformat

from django import template


register = template.Library()


@register.filter(name='money_format')
def money_format(value):
    return mformat(value)
