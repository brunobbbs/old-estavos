# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from pagseguro.signals import notificacao_recebida
from .usernotification import mail_confirmed_inscription
from .models import CompetitorsResponsible


def update_status(sender, transaction, **kwargs):
    reference = int(transaction['reference'])
    payment_status = str(transaction['status'])
    obj = get_object_or_404(CompetitorsResponsible, pk=reference)
    obj.status = payment_status
    if payment_status == '3' or payment_status == '4':
        obj.paid = True
        mail_confirmed_inscription(obj.name, obj.email, 'paid')
    else:
        obj.paid = False
    obj.save()


notificacao_recebida.connect(update_status)