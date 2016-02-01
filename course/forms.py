# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import EmailMultiAlternatives
from captcha.fields import ReCaptchaField

from .models import Subscription, Student
from portal.models import CourseLead


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('name', 'age')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseSubscriptionForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Subscription
        fields = ('course', 'name', 'email', 'phone', 'captcha')
        exclude = ('identifier', 'state', 'city', 'cep', 'address', 'cpf', 'birthday')
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'student': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def subscription_alert(self):
        data = self.cleaned_data
        name = data['name']
        student = data['student']
        age = data['age']

        message = u'''Olá equipe,
        Acabamos de receber uma nova inscrição no Curso de Xadrez.
        {0} inscreveu o aluno {1} de {2} anos.
        Acesse o painel administrativo para mais informações e cheque o estado do pagamento no pagseguro.
        Vamos levar o Xadrez para todos!
        '''.format(name, student, age)

        html_message = u'''
        <p>Olá equipe,</p>
        <p>Acabamos de receber uma nova inscrição no Curso de Xadrez.</p>
        <p><strong>{0}</strong> inscreveu o aluno <strong>{1}</strong> de <strong>{2} anos de idade</strong>.</p>
        <p>Acesse o painel administrativo para mais informações e cheque o estado do pagamento no pagseguro.</p>
        <p>Vamos levar o Xadrez para todos!</p>
        '''.format(name, student, age)

        recipient_list = ["diretoria@estavos.com", ]

        email_ = EmailMultiAlternatives(
            subject=u"Nova inscrição no Curso de Xadrez",
            body=message,
            from_email='no-reply@estavos.com',
            to=recipient_list,
            headers={'Reply-To': "diretoria@estavos.com"}
        )
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return

    def client_subscription_mail(self):
        data = self.cleaned_data
        name = data['name']
        email = data['email']

        message = u'''Olá {0},
        Parabéns pela excelente escolha! Você verá como o Xadrez pode mudar sua vida para melhor.
        Nós recebemos seu pedido de inscrição e informamos que ele encontra-se em processamento.
        Assim que sua matrícula estiver confirmada nós lhe enviaremos um email avisando.
        Isso pode levar de 1 a 2 dias úteis ok?
        Lembramos que nosso primeiro encontro será no dia 03/10/2015 (sábado) das 9h às 12h no Núcleo de Xadrez da ASCADE.
        O endereço é Setor de Clubes Sul - trecho 2, Conjunto 10, Lote 18 - Asa Sul, Brasília - DF.
        Se tiver qualquer dúvida, não deixe de entrar em <a href="{1}">contato</a>.
        Atenciosamente,
        Bruno Barbosa, Diretor Administrativo - Academia ESTAVOS
        '''.format(name, "http://estavos.com/contato/")

        html_message = u'''
        <p>Olá {0},</p>
        <p>Parabéns pela excelente escolha! Você verá como o Xadrez pode mudar sua vida para melhor.</p>
        <p>Nós recebemos seu pedido de inscrição e informamos que ele encontra-se em processamento.</p>
        <p>Assim que sua matrícula estiver confirmada nós lhe enviaremos um email avisando.</p>
        <p>Isso pode levar de 1 a 2 dias úteis ok?</p>
        <p>Lembramos que nosso primeiro encontro será no dia <strong>03/10/2015 (Sábado)</strong> das <strong>9h às 12h</strong> no <strong>Núcleo de Xadrez do Clube ASCADE</strong><p>
        <p>O endereço é Setor de Clubes Sul - trecho 2, Conjunto 10, Lote 18 - Asa Sul, Brasília - DF.
        <p>Se tiver qualquer dúvida, não deixe de entrar em <a href="{1}">contato</a>.</p>
        <p>Atenciosamente,</p>
        <p>Bruno Barbosa <br />
        <em>Diretor Administrativo</em><br />
        Academia ESTAVOS<br />
        <a href="http://estavos.com">http://estavos.com</a><br />
        contato@estavos.com</p>
        '''.format(name, "http://estavos.com/contato/")

        recipient_list = [email, ]

        email_ = EmailMultiAlternatives(
            subject=u"Inscrição no Curso de Xadrez para Iniciantes",
            body=message,
            from_email='no-reply@estavos.com',
            to=recipient_list,
            headers={'Reply-To': "contato@estavos.com"}
        )
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return


class CourseLeadForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = CourseLead
        fields = ('name', 'email', 'phone', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
