# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PortalConfig(AppConfig):
    name = 'account'
    verbose_name = _(u"Contas de usuário")
