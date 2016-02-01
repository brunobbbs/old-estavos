# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    name = models.CharField(_(u"Nome do curso"), max_length=150)
    start_date = models.DateField(_(u"Data de início"))
    place = models.CharField(_(u"Local"), max_length=50)
    period = models.CharField(_(u"Horários"), max_length=50)
    price = models.DecimalField(_(u"Preço"), max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = _(u"Curso")
        verbose_name_plural = _(u"Cursos")

    def __unicode__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(_(u"Nome do aluno"), max_length=150)
    age = models.PositiveIntegerField(_(u"Idade"))
    subscription = models.ForeignKey("course.Subscription", related_name='students')

    class Meta:
        verbose_name = _(u"Aluno")
        verbose_name_plural = _(u"Alunos")

    def __unicode__(self):
        return self.name


class Subscription(models.Model):

    STATUS = (
        ("1", "Aguardando pagamento"),
        ("2", "Em análise"),
        ("3", "Paga"),
        ("4", "Disponível"),
        ("5", "Em disputa"),
        ("6", "Devolvida"),
        ("7", "Cancelada"),
    )
    identifier = models.CharField(max_length=50, blank=True)
    name = models.CharField(_(u"Nome completo"), max_length=150)
    email = models.EmailField()
    phone = models.CharField(_(u"Telefone"), max_length=15)
    cpf = models.CharField(_("CPF"), max_length=14, blank=True)
    birthday = models.DateField(_(u"Data de nascimento"), null=True, blank=True)
    state = models.CharField(_(u"Estado"), max_length=2, default="DF")
    city = models.CharField(_(u"Cidade"), max_length=50, blank=True)
    cep = models.CharField(_(u"CEP"), max_length=10, blank=True)
    address = models.CharField(_(u"Endereço"), max_length=200, blank=True)

    subscription_date = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey("course.Course", related_name="subscriptions", verbose_name="Curso")
    status = models.CharField(max_length=1, choices=STATUS, default="1")
    transaction = models.CharField(max_length=100, blank=True)

    class Meta:
        permissions = (
            ("view_coursesubscription", _(u"Can view CourseSubscription")),
        )
        verbose_name = _(u"Inscriçao")
        verbose_name_plural = _(u"Inscrições")

    def __unicode__(self):
        return self.name
