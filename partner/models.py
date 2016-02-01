# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Partner(models.Model):
    """ """
    name = models.CharField(
        _(u"Instituição"),
        max_length=50
    )
    email = models.EmailField(_(u"Email"))
    contact = models.CharField(
        _(u"Contato"),
        max_length=50
    )
    phone = models.CharField(
        _(u"Telefone"),
        max_length=15
    )
    logo = models.ImageField(
        _(u"Logo"),
        upload_to="partners/"
    )
    alt = models.CharField(
        _(u"Texto alternativo"),
        max_length=50
    )
    site = models.URLField(
        _(u"Site"),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _(u"Parceiro")
        verbose_name_plural = _(u"Parceiros")

    def __unicode__(self):
        return self.name
