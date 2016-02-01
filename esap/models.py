# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import pluralize

from utils.slug import unique_slugify
from utils.current_user import get_current_user


class OrderedByModifiedDateManager(models.Manager):
    def get_queryset(self):
        return super(OrderedByModifiedDateManager, self). get_queryset().order_by('-modified')


class Keyword(models.Model):
    """ """
    name = models.CharField(
        _(u'Nome'),
        max_length=50
    )
    slug = models.SlugField(unique=True)

    class Meta:
        permissions = (
            ("view_keyword", _(u"Can view Keyword")),
        )
        verbose_name = _(u"Keyword")
        verbose_name_plural = _(u"Keywords")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return reverse('dashboard:keyword_detail', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        slug = u"{0}".format(self.name.lower())
        unique_slugify(self, slug)
        super(Keyword, self).save()


class Classes(models.Model):
    """ """
    LEVELS = (
        ("standard", _(u"Iniciante")),
        ("intermediate", _(u"Intermediário")),
        ("advanced", _(u"Avançado"))
    )
    CATEGORY = (
        ("opening", _(u"Abertura")),
        ("middlegame", _(u"Meio-Jogo")),
        ("end", _(u"Final")),
        ("rules", _(u"Regras")),
        ("other", _(u"Outros"))
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"Autor")
    )
    title = models.CharField(
        _(u"Título"),
        max_length=50
    )
    description = models.CharField(
        _(u"Descrição"),
        max_length=100,
        blank=True,
        null=True,
    )
    time = models.IntegerField(
        _(u"Tempo"),
        default=60,
        help_text=_(u"Informe a duração da aula em minutos.")
    )
    category = models.CharField(
        _(u"Categoria"),
        max_length=10,
        help_text=_(u"Em qual fase do jogo esta aula se encontra?"),
        choices=CATEGORY
    )
    level = models.CharField(
        _(u"Nível"),
        max_length=12,
        choices=LEVELS
    )
    content = models.TextField(_(u"Conteúdo proposto"))
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name=_(u"Palavras-chave"),
        blank=True,
    )
    objective = models.TextField(
        _(u"Objetivo"),
        blank=True,
        null=True,
        default=_(u"Nenhum objetivo cadastrado")
    )
    didatic = models.TextField(
        _(u"Didática"),
        blank=True,
        null=True,
        default=_(u"Nenhuma didática cadastrada")
    )
    method = models.TextField(
        _(u"Método"),
        blank=True,
        null=True,
        default=_(u"Nenhum método cadastrado")
    )
    created = models.DateTimeField(
        auto_now_add=True,
        blank=True
    )
    modified = models.DateTimeField(
        auto_now=True,
        blank=True
    )
    last_update = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"Última atualização"),
        related_name='last_user_update'
    )
    status = models.BooleanField(
        _(u"Ativo?"),
        blank=True,
        default=False
    )

    class Meta:
        permissions = (
            ("view_classes", _(u"Can view Aula")),
        )
        verbose_name = _(u"Aula")
        verbose_name_plural = _(u"Aulas")
        get_latest_by = 'modified'

    objects = OrderedByModifiedDateManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if not self.pk:
            self.author = current_user
        self.last_update = current_user
        super(Classes, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return reverse('dashboard:classes_detail', kwargs={'pk': self.pk})

    def new(self):
        new = timezone.now() - timedelta(days=3)
        if self.modified > new:
            return True
        return False

    def is_active(self):
        return self.status

    def materials_count(self):
        qs = SupportMaterial.objects.filter(classes__exact=self.pk).count()
        return qs


class SupportMaterial(models.Model):
    """ """
    title = models.CharField(
        _(u"Título"),
        max_length=50
    )
    description = models.CharField(
        _(u"Descrição"),
        max_length=100,
        blank=True,
        null=True
    )
    file = models.FileField(
        _(u"Arquivo"),
        upload_to="supportmaterial/"
    )
    pgn = models.BooleanField(
        _(u"PGN"),
        default=False,
        blank=True,
        help_text=_(u"Marque se for um arquivo PGN.")
    )
    classes = models.ForeignKey(
        Classes,
        blank=True,
        null=True
    )

    class Meta:
        permissions = (
            ("view_supportmaterial", _(u"Can view Material de apoio")),
        )
        verbose_name = _(u"Material de apoio")
        verbose_name_plural = _(u"Materiais de apoio")

    def __unicode__(self):
        return self.title


class Module(models.Model):
    """ """
    FREQUENCIES = (
        ('w', _(u"Semanal")),
        ('m', _(u"Mensal"))
    )
    LEVELS = (
        ("standard", _(u"Iniciante")),
        ("intermediate", _(u"Intermediário")),
        ("advanced", _(u"Avançado"))
    )

    title = models.CharField(
        _(u"Título"),
        max_length=50
    )
    level = models.CharField(
        _(u"Nível"),
        max_length=12,
        choices=LEVELS,
        default="standard"
    )
    profile = models.TextField(
        _(u"Perfil"),
        blank=True,
        null=True
    )
    frequency = models.IntegerField(
        _(u"Sugestão de frequência"),
        help_text=_(u"Informe a quantidade de encontros sugeridos para este módulo")
    )
    frequency2 = models.CharField(
        _(u"Tipo de frequência"),
        max_length=1,
        choices=FREQUENCIES
    )
    value = models.DecimalField(
        _(u"Valor (R$)"),
        help_text=_(u"Quanto custa esse módulo? Ex.: 1200.00"),
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )
    disccount = models.IntegerField(
        _(u"% Desconto"),
        help_text=_(u"Informe o valor do desconto para pagamento à vista (%)"),
        blank=True,
        null=True,
        default=10
    )
    classes = models.ManyToManyField(
        Classes,
        verbose_name=_(u"Aulas")
    )
    considerations = models.TextField(
        _(u"Considerações"),
        blank=True,
        null=True
    )
    curiosity = models.TextField(
        _(u"Curiosidade"),
        blank=True,
        null=True
    )
    image = models.ImageField(
        _(u"Imagem"),
        help_text=_(u"Envie uma imagem que represente o módulo"),
        blank=True,
        null=True,
        upload_to="module_images/"
    )
    active = models.BooleanField(
        _(u"Ativo?"),
        blank=True,
        default=False,
        help_text=_(u"Marque se o pacote estiver ativo.")
    )

    class Meta:
        permissions = (
            ("view_module", _(u"Can view Módulo")),
        )
        verbose_name = _(u"Módulo")
        verbose_name_plural = _(u"Módulos")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return reverse('dashboard:module_detail', kwargs={'pk': self.pk})

    def classes_count(self):
        return self.classes.count()

    def module_duration(self):
        duration = int()
        classes = self.classes.select_related()
        for klass in classes:
            duration += klass.time
        result = duration / 60
        return _(u"{0} hora{1}/aula".format(result, pluralize(result)))


class Plan(models.Model):
    """ """
    type_plan = models.CharField(
        _(u"Tipo de parcelamento"),
        max_length=50
    )
    quantity = models.IntegerField(_(u"Quantidade"))
    module = models.ForeignKey(
        Module,
        verbose_name=_(u"Módulo"),
        related_name="plans"
    )

    class Meta:
        permissions = (
            ("view_plan", _(u"Can view Parcelamento")),
        )
        verbose_name = _(u"Parcelamento")
        verbose_name_plural = _(u"Parcelamentos")

    def __unicode__(self):
        return self.type_plan


class Instructor(models.Model):
    """ """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"Usuário")
    )
    state = models.ForeignKey("core.State", verbose_name="Estado", related_name="instructors")
    city = models.CharField(_(u"Cidade"), max_length=45)
    district = models.CharField(_(u"Bairro"), max_length=45)
    address = models.CharField(_(u"Endereço"), max_length=100)
    complement = models.CharField(_(u"Complemento"), max_length=45, blank=True)
    cep = models.CharField(_(u"CEP"), max_length=10)
    rg = models.CharField(_(u"RG"), max_length=20)
    cpf = models.CharField(_(u"CPF"), max_length=14)
    phone1 = models.CharField(_(u"Telefone 1"), max_length=15)
    phone2 = models.CharField(_(u"Telefone 2"), max_length=15, blank=True)
    photo = models.ImageField(
        _(u"Foto"),
        blank=True,
        null=True,
        upload_to="instructors/"
    )

    class Meta:
        permissions = (
            ("view_instructor", _(u"Can view Instructor")),
        )
        verbose_name = _(u"Instrutor")
        verbose_name_plural = _(u"Instrutores")

    def __unicode__(self):
        return self.user.first_name

    @models.permalink
    def get_absolute_url(self):
        return reverse('dashboard:instructor_detail', kwargs={'pk': self.pk})


class ParticularClient(models.Model):
    """ """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"Email")
    )
    fullname = models.CharField(
        _(u"Nome completo"),
        max_length=100,
        blank=True
    )
    occupation = models.CharField(_(u"Profissão"), max_length=45, blank=True)
    state = models.ForeignKey("core.State", verbose_name="Estado", related_name="particular_clients")
    city = models.CharField(_(u"Cidade"), max_length=45)
    district = models.CharField(_(u"Bairro"), max_length=45)
    address = models.CharField(_(u"Endereço"), max_length=100)
    complement = models.CharField(_(u"Complemento"), max_length=45, blank=True)
    cep = models.CharField(_(u"CEP"), max_length=10, blank=True)
    rg = models.CharField(_(u"RG"), max_length=20, blank=True)
    uf_sender = models.CharField(_(u"Órgão emissor"), max_length=10, blank=True)
    cpf = models.CharField(_(u"CPF"), max_length=14, blank=True)
    phone1 = models.CharField(_(u"Telefone 1"), max_length=15)
    phone2 = models.CharField(_(u"Telefone 2"), max_length=15, blank=True)
    nationality = models.CharField(_(u"Nacionalidade"), max_length=45, blank=True)
    marital_status = models.CharField(_(u"Estado civil"), max_length=25)  # TODO: check choices for it
    naturality = models.CharField(_(u"Naturalidade"), max_length=45, blank=True)
    uf_naturality = models.ForeignKey("core.State", verbose_name="UF Naturalidade", blank=True, null=True)

    class Meta:
        permissions = (
            ("view_particularclient", _(u"Can view ParticularClient")),
        )
        verbose_name = _(u"Cliente particular")
        verbose_name_plural = _(u"Clientes particulares")

    def __unicode__(self):
        return self.user.get_full_name

    # @models.permalink
    # def get_absolute_url(self):
    #     return reverse('dashboard:particularclient_detail', kwargs={'pk': self.pk})
