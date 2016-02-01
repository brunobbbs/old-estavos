# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.filter(name='label_category')
def label_category(value):
    labels = {
        "opening": "info",
        "middlegame": "primary",
        "end": "success",
        "rules": "warning",
        "other": "default"
    }
    return labels.get(value, 'warning')


@register.filter(name='label_status')
def label_status(value):
    return value and 'Ativo' or 'Inativo'


@register.filter(name='label_status_color')
def label_status_color(value):
    return value and 'label label-success' or 'label'


@register.filter(name='label_levels')
def label_levels(value):
    labels = {
        "standard": "info",
        "intermediate": "primary",
        "advanced": "success",
    }
    return labels.get(value, 'warning')
