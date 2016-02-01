# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import ReCaptchaField
from django.core.mail import EmailMultiAlternatives
from .models import CompetitorsResponsible, Competitor


class CompetitorsResponsibleForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = CompetitorsResponsible
        fields = [
            'competition', 'name', 'email', 'captcha'
        ]
        exclude = [
            'paid', 'inscription_date', 'status',
            'transaction', 'payment_type', 'receipt'
        ]
        widgets = {
            'competition': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def inscription_mail(self):
        data = self.cleaned_data
        name = data['name']
        email = data['email']

        message = u'''Olá {0}, tudo bem?
        Nós recebemos seu pedido de pré-inscrição.
        Lembre-se que a inscrição só será válida após confirmação de pagamento.
        Você poderá verificar o andamento de sua inscrição a qualquer momento em nosso site. (estavos.com)
        O torneio acontecerá no dia 06 de Dezembro de 2015 no SESI de Taguatinga
        (QNF 24 Área Especial - Taguatinga Norte - 72125-740)
        Se tiver qualquer dúvida, não deixe de entrar em contato: contato@estavos.com.
        Atenciosamente,
        Bruno Barbosa - Academia ESTAVOS
        '''.format(name, "http://estavos.com/contato/")

        html_message = u'''
        <p>Olá {0}, tudo bem?</p>
        <p>Nós recebemos seu pedido de pré-inscrição.</p>
        <p>Lembre-se que a inscrição só será válida após confirmação de pagamento.</p>
        <p>Você poderá <a href="{2}">verificar o andamento de sua inscrição</a> a qualquer momento em nosso site.</p>
        <p>O torneio acontecerá no dia 06 de Dezembro de 2015 no SESI de Taguatinga</p>
        <p>QNF 24 Área Especial - Taguatinga Norte - 72125-740<p>
        <p>Se tiver qualquer dúvida, não deixe de entrar em <a href="{1}">contato</a>.</p>
        <p>Atenciosamente,</p>
        <p>Bruno Barbosa <br />
        Academia ESTAVOS<br />
        <a href="http://estavos.com">http://estavos.com</a><br />
        contato@estavos.com</p>
        '''.format(
            name,
            "http://estavos.com/contato/",
            "http://estavos.com/torneios/festival-de-xadrez/checar-inscricao/"
        )

        recipient_list = [email, ]

        email_ = EmailMultiAlternatives(
            subject=u"Pré-inscrição recebida - Festival de Xadrez da Família",
            body=message,
            from_email='no-reply@estavos.com',
            to=recipient_list,
            headers={'Reply-To': "contato@estavos.com"}
        )
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return


class DepositPaymentForm(forms.ModelForm):

    class Meta:
        model = CompetitorsResponsible
        fields = ['payment_type', ]
        exclude = [
            'competition', 'name', 'email',
            'paid', 'inscription_date', 'status',
            'transaction', 'receipt',
        ]
        widgets = {
            'payment_type': forms.HiddenInput(),
        }


class CompetitorForm(forms.ModelForm):

    class Meta:
        model = Competitor
        fields = [
            'name', 'birth', 'school'
        ]
        exclude = ['responsible', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth': forms.DateInput(attrs={'class': 'form-control birth'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CheckInscriptionForm(forms.Form):

    email = forms.EmailField()
    captcha = ReCaptchaField()
