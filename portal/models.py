# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models


class Service(models.Model):
    """
    """
    title = models.CharField(
        _(u"Título"),
        max_length=50,
        help_text=_(u"Nome do serviço")
    )
    description = models.CharField(
        _(u"Descrição"),
        max_length=150, blank=True, null=True,
        help_text=_(u"Descrição do serviço")
    )
    cover = models.ImageField(
        _(u"Imagem de capa"),
        upload_to='cover/',
        help_text=_(u"Imagem de capa da página do serviço")
    )
    text = tinymce_models.HTMLField(_(u'Texto'))
    gallery = models.ForeignKey(
        'galeria.Gallery',
        verbose_name=_(u"Galeria"),
        help_text=_(u"Escolha uma galeria de imagens para exibir na página")
    )
    effect_text = models.CharField(
        _(u"Texto de efeito"),
        max_length=150, null=True, blank=True,
        help_text=_(u"Um texto de impacto com intuito de chamar o cliente")
    )
    slug = models.SlugField(
        _(u"URL"),
        max_length=100, unique=True, db_index=True,
        help_text=_(u"Não altere este campo a menos que saiba o que está fazendo!")
    )

    class Meta:
        verbose_name = _(u"Serviço")
        verbose_name_plural = _(u"Serviços")
        ordering = ('title', )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'services:service-detail', (), {'slug': self.slug}

    def get_random_image(self):
        return self.gallery.images.all().order_by('?')[0]


class Quote(models.Model):
    """ """
    quote = models.TextField(_(u"Frase"))
    author = models.CharField(
        _(u"Autor"),
        max_length=50
    )
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u"Frase")
        verbose_name_plural = _(u"Frases")
        ordering = ('created', )

    def __unicode__(self):
        return self.author


class AboutUs(models.Model):
    """ """
    title = models.CharField(
        _(u"Título"),
        max_length=150
    )
    description = models.TextField(_(u"Descrição"))
    text = tinymce_models.HTMLField(_(u'Texto'))
    gallery = models.ForeignKey(
        'galeria.Gallery',
        verbose_name=_(u"Galeria"),
        help_text=_(u"Escolha uma galeria de imagens para exibir na página")
    )

    class Meta:
        verbose_name = _(u"Quem Somos")
        verbose_name_plural = _(u"Quem Somos")

    def __unicode__(self):
        return self.title


class Testimonial(models.Model):
    """ """
    title = models.CharField(
        _(u"Título"),
        max_length=100
    )
    testimonial = models.TextField(_(u"Depoimento"))
    author = models.CharField(
        _(u"Autor"),
        max_length=50
    )
    complementary = models.CharField(
        _(u"Informação complementar"),
        null=True,
        blank=True,
        max_length=100,
        help_text=_(u"Ex.: Pai de Fulano, 7 anos.")
    )
    photo = models.ImageField(
        _(u"Foto"),
        blank=True,
        null=True,
        upload_to="testimonials/"
    )

    class Meta:
        verbose_name = _(u"Depoimento")
        verbose_name_plural = _(u"Depoimentos")

    def __unicode__(self):
        return self.title


class Talent(models.Model):
    """ """
    name = models.CharField(
        _(u"Nome completo"),
        max_length=150
    )
    address = models.CharField(
        _(u"Endereço"),
        max_length=100
    )
    complement = models.CharField(
        _(u"Complemento"),
        max_length=50,
        blank=True,
        null=True
    )
    district = models.CharField(
        _(u"Bairro"),
        max_length=100
    )
    city = models.CharField(
        _(u"Cidade"),
        max_length=100
    )
    state = models.ForeignKey(
        'core.State',
        verbose_name=_(u"Estado")
    )
    birth = models.DateField(_(u"Data de nascimento"))
    phone = models.CharField(
        _(u"Telefone"),
        max_length=15,
        blank=True,
        null=True
    )
    mobile = models.CharField(
        _(u"Celular"),
        max_length=15
    )
    email = models.EmailField()
    resume = models.FileField(
        _(u"Currículo"),
        upload_to='curriculos/'
    )
    week_morning = models.BooleanField(
        _(u"Maior disponibilidade no período matutino"),
        default=True,
        blank=True
    )
    week_afternoon = models.BooleanField(
        _(u"Maior disponibilidade no período vespertino"),
        default=True,
        blank=True
    )
    weekend = models.BooleanField(
        _(u"Disponibilidade para trabalhar aos finais de semana"),
        default=False,
        blank=True
    )
    added = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _(u"Talento")
        verbose_name_plural = _(u"Talentos")

    def __unicode__(self):
        return self.name


class CourseLead(models.Model):
    name = models.CharField(_(u"Nome"), max_length=100)
    email = models.EmailField()
    phone = models.CharField(_(u"Telefone"), max_length=15, blank=True, null=True)

    class Meta:
        permissions = (
            ("view_courselead", _(u"Can view CourseLead")),
        )
        verbose_name = _(u"Cliente potencial")
        verbose_name_plural = _(u"Clientes potenciais")

    def __unicode__(self):
        return self.name
