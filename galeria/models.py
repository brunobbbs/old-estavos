# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Image(models.Model):
    """ """
    title = models.CharField(
        _(u"Título"),
        max_length=50
    )
    description = models.TextField(
        _(u"Descrição"),
        blank=True,
        null=True
    )
    file = models.ImageField(
        _(u"Imagem"),
        upload_to='images/'
    )

    class Meta:
        verbose_name = _(u"Imagem")
        verbose_name_plural = _(u"Imagens")
        ordering = ('title', )

    def __unicode__(self):
        return self.title


class Gallery(models.Model):
    """ """
    title = models.CharField(
        _(u"Título"),
        max_length=50
    )
    description = models.TextField(
        _(u"Descrição"),
        blank=True,
        null=True
    )
    images = models.ManyToManyField(
        Image,
        verbose_name=_(u"Imagens")
    )

    class Meta:
        verbose_name = _(u"Galeria")
        verbose_name_plural = _(u"Galerias")
        ordering = ('title', )

    def __unicode__(self):
        return self.title

    def count_images(self):
        return self.images.count()
    count_images.short_description = _(u"Total de imagens")
