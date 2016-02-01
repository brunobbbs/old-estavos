# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget

from .models import *


class KeywordForm(forms.ModelForm):

    class Meta:
        model = Keyword
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SupportMaterialForm(forms.ModelForm):

    class Meta:
        model = SupportMaterial
        fields = ('title', 'description', 'file', 'pgn')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pgn': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class ClassesBaseForm(forms.Form):
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
        ("other", _(u"Outras"))
    )
    title = forms.CharField(
        label=_(u"Título"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
    )
    description = forms.CharField(
        label=_(u"Descrição"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
    )
    time = forms.IntegerField(
        label=_(u"Tempo"),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=60,
        help_text=_(u"Informe a duração da aula em minutos.")
    )
    category = forms.ChoiceField(
        label=_(u"Categoria"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CATEGORY,
        help_text=_(u"Em qual fase do jogo esta aula se encontra?")
    )
    level = forms.ChoiceField(
        label=_(u"Nível"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=LEVELS
    )
    content = forms.CharField(
        label=_(u"Conteúdo proposto"),
        widget=SummernoteWidget(attrs={'class': 'form-control'})
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        label=_(u"Palavras-chave"),
        # to_field_name="slug",
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control chosen-select',
                'data-placeholder': 'Digite as palavras-chave',
                'style': 'width:350px;',
                'tabindex': '4'
            }
        ),
        required=False,
    )


class ClassesForm(forms.ModelForm):

    class Meta:
        model = Classes
        fields = ('title', 'description', 'time', 'category', 'level', 'content', 'keywords')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.NumberInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),
            'keywords': forms.SelectMultiple(
                attrs={
                    'class': 'form-control chosen-select',
                    'data-placeholder': 'Digite as palavras-chave',
                    'style': 'width:350px;',
                    'tabindex': '4'
                },
            ),
        }


class ClassesAjaxUpdateForm(forms.ModelForm):

    class Meta:
        model = Classes
        fields = ('title', 'time', 'category', 'level', 'content',
                  'objective', 'didatic', 'method')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.NumberInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),
            'objective': SummernoteWidget(attrs={'class': 'form-control'}),
            'didatic': SummernoteWidget(attrs={'class': 'form-control'}),
            'method': SummernoteWidget(attrs={'class': 'form-control'}),
        }


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ('type_plan', 'quantity')
        widgets = {
            'type_plan': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ModuleBaseForm(forms.Form):
    """ """
    LEVELS = (
        ("standard", _(u"Iniciante")),
        ("intermediate", _(u"Intermediário")),
        ("advanced", _(u"Avançado"))
    )
    FREQUENCIES = (
        ('w', _(u"Semanal")),
        ('m', _(u"Mensal"))
    )
    title = forms.CharField(
        label=_(u"Título"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
    )
    level = forms.ChoiceField(
        label=_(u"Nível"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=LEVELS
    )
    frequency = forms.IntegerField(
        label=_(u"Sugestão de frequência"),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        help_text=_(u"Informe a quantidade de encontros sugeridos para este módulo")
    )
    frequency2 = forms.ChoiceField(
        label=_(u"Tipo de frequência"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=FREQUENCIES,
        help_text=_(u"Este módulo é melhor aproveitado com aulas semanais/mensais?")
    )
    value = forms.RegexField(
        regex='^[0-9]{1,10}.[0-9]{2}$',
        label=_(u"Valor (R$)"),
        help_text=_(u"Quanto custa esse módulo? Ex.: 1200.00"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
    )
    classes = forms.ModelMultipleChoiceField(
        queryset=Classes.objects.all(),
        label=_(u"Aulas deste módulo"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control chosen-select',
                'data-placeholder': 'Informe as aulas deste módulo',
                'style': 'width:350px;',
                'tabindex': '4'
            }
        ),
    )


class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('title', 'level', 'frequency', 'frequency2', 'value', 'classes')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency2': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'classes': forms.SelectMultiple(
                attrs={
                    'class': 'form-control chosen-select',
                    'data-placeholder': 'Informe as aulas deste módulo',
                    'style': 'width:350px;',
                    'tabindex': '4'
                },
            ),
        }


class ModuleAjaxUpdateForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('title', 'level', 'frequency', 'frequency2', 'profile',
                  'considerations', 'curiosity', 'classes')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency2': forms.TextInput(attrs={'class': 'form-control'}),
            'profile': SummernoteWidget(attrs={'class': 'form-control'}),
            'considerations': SummernoteWidget(attrs={'class': 'form-control'}),
            'curiosity': SummernoteWidget(attrs={'class': 'form-control'}),
            'classes': forms.SelectMultiple(
                attrs={
                    'class': 'form-control chosen-select',
                    'data-placeholder': 'Informe as aulas deste módulo',
                    'style': 'width:350px;',
                    'tabindex': '4'
                },
            ),
        }


class InstructorForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = (
            'user', 'state', 'city', 'district', 'address', 'complement',
            'cep', 'rg', 'cpf', 'phone1', 'phone2', 'photo'
        )
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone1': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ParticularClientForm(forms.ModelForm):

    class Meta:
        model = ParticularClient
        fields = (
            'user', 'fullname', 'occupation', 'state', 'city', 'district',
            'address', 'complement', 'cep', 'rg', 'uf_sender', 'cpf', 'phone1',
            'phone2', 'nationality', 'marital_status', 'naturality', 'uf_naturality',
        )
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'uf_sender': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone1': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.TextInput(attrs={'class': 'form-control'}),
            'naturality': forms.TextInput(attrs={'class': 'form-control'}),
            'uf_naturality': forms.Select(attrs={'class': 'form-control'}),
        }
