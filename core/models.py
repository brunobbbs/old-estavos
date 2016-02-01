# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):

    name = models.CharField(
        _(u"Nome"),
        max_length=50
    )

    class Meta:
        verbose_name = _(u"País")
        verbose_name_plural = _(u"Países")

    def __unicode__(self):
        return self.name


class State(models.Model):

    country_id = models.ForeignKey(
        'core.Country',
        verbose_name=_(u"País")
    )
    sigla = models.CharField(
        _(u"Sigla"),
        max_length=2
    )
    name = models.CharField(
        _(u"Nome"),
        max_length=50
    )

    class Meta:
        verbose_name = _(u"Estado")
        verbose_name_plural = _(u"Estados")
        ordering = ["name", ]

    def __unicode__(self):
        return u"{0} - {1}".format(self.sigla, self.name)

    def save(self, *args, **kwargs):
        self.sigla = self.sigla.upper()
        super(State, self).save(*args, **kwargs)
