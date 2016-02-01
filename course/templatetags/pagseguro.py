# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.filter(name='payment_status')
def payment_status(value):
    labels = {
        "1": "Cartão de crédito",
        "2": "Boleto",
        "3": "Débito online (TEF)",
        "4": "Saldo PagSeguro",
        "5": "Oi Paggo",
        "7": "Depósito em conta",
    }
    return labels.get(value)
