# -*- coding: utf-8 -*-

from partner.models import Partner
from portal.models import Quote, Service


def all_pages(request):
    qs = Quote.objects.all().order_by('?')
    if qs:
        qs = qs[0]
    context_vars = {
        'service_pages': Service.objects.all(),
        'quote': qs,
        'partners': Partner.objects.all()
    }
    return context_vars
