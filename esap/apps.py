# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PortalConfig(AppConfig):
    name = 'esap'
    verbose_name = _(u"ESTAVOS - Sistema de Aulas Particulares")
