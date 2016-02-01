# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from .manager import CompetitorQuerySet, CompetitorsResponsibleQuerySet


@python_2_unicode_compatible
class Tournament(models.Model):
    name = models.CharField(_('Nome do torneio'), max_length=100)
    price = models.DecimalField(
        _(u"Valor da inscrição"),
        max_digits=7,
        decimal_places=2,
        default='20.00'
    )
    date = models.DateField(_('Data do torneio'))

    class Meta:
        db_table = 'tournament'
        verbose_name = _('Torneio')
        verbose_name_plural = _('Torneios')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CompetitorsResponsible(models.Model):

    STATUS = (
        ("1", "Aguardando pagamento"),
        ("2", "Em análise"),
        ("3", "Paga"),
        ("4", "Disponível"),
        ("5", "Em disputa"),
        ("6", "Devolvida"),
        ("7", "Cancelada"),
    )

    P_TYPE = (
        ('1', _('PagSeguro')),
        ('2', _('Depósito bancário/Transferência')),
        ('3', _('Isenção'))
    )

    name = models.CharField(_('Nome do pai/mãe ou responsável'), max_length=100)
    email = models.EmailField(_('Email'))
    competition = models.ForeignKey(
        'tournament.Tournament',
        verbose_name=_('Competição'),
        related_name='responsibles'
    )
    paid = models.BooleanField(_('Pago?'), default=False)
    payment_type = models.CharField(
        _('Forma de pagamento'),
        max_length=1,
        choices=P_TYPE,
        default='1'
    )
    receipt = models.FileField(
        upload_to='chessfamily2015/receipts/',
        verbose_name=_('Recibo'),
        blank=True,
        null=True,
    )
    inscription_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Data/Hora inscrição'))
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    transaction = models.CharField(max_length=100, blank=True)

    objects = models.Manager()
    inscriptions = CompetitorsResponsibleQuerySet.as_manager()

    class Meta:
        verbose_name = _('Responsável')
        verbose_name_plural = _('Responsáveis')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Competitor(models.Model):
    responsible = models.ForeignKey(
        'tournament.CompetitorsResponsible',
        blank=True,
        null=True,
        verbose_name=_('Responsável'),
        related_name='competitors'
    )
    name = models.CharField(_('Nome'), max_length=150)
    birth = models.DateField(_('Data de nascimento'))
    school = models.CharField(
        _('Escola/Clube'),
        blank=True,
        null=True,
        max_length=50
    )

    objects = models.Manager()
    modality = CompetitorQuerySet.as_manager()

    class Meta:
        db_table = 'competitors'
        verbose_name = _('Competidor')
        verbose_name_plural = _('Competidores')
        ordering = ['name', 'birth']

    def __str__(self):
        return self.name

    def category_name(self):
        if self.birth.year >= 2008:
            return 'sub-07'

        elif self.birth.year >= 2006 and self.birth.year <= 2007:
            return 'sub-09'

        elif self.birth.year >= 2003 and self.birth.year <= 2005:
            return 'sub-12'

        elif self.birth.year >= 2000 and self.birth.year <= 2002:
            return 'sub-15'

        elif self.birth.year >= 1997 and self.birth.year <= 1999:
            return 'sub-18'

        else:
            return 'absoluto'

    category_name.short_description = 'Categoria'
