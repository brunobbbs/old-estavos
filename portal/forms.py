# -*- coding: utf-8 -*-

from datetime import datetime
from django import forms
from django.core.mail import EmailMultiAlternatives
from captcha.fields import ReCaptchaField

from portal.models import Talent, CourseLead


class ContactForm(forms.Form):
    """ """
    # https://docs.djangoproject.com/en/1.7/topics/forms/#using-a-form-in-a-view
    # https://docs.djangoproject.com/en/1.7/ref/forms/widgets/
    name = forms.CharField(label="Nome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    mail = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Telefone", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label="Assunto", widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Mensagem", widget=forms.Textarea(attrs={'class': 'form-control'}))
    cc_myself = forms.BooleanField(label="Enviar uma cópia para mim", required=False)
    captcha = ReCaptchaField()

    def send_mail(self):
        # https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/
        # https://docs.djangoproject.com/en/1.7/topics/email/
        data = self.cleaned_data
        name = data['name']
        email = data['mail']
        phone = data['phone']
        subject = data['subject']
        message = data['message']
        cc_myself = data['cc_myself']

        html_message = u'''
        ** Contato a partir do Site Institucional feito em {0} ** <br />
        Nome: {1} <br />
        Email: {2} <br />
        Telefone: {3} <br />
        Mensagem: {4} <br />
        '''.format(datetime.now().strftime("%d/%m/%Y"), name, email, phone, message)

        recipient_list = ['contato@estavos.com', ]
        if cc_myself:
            recipient_list.append(email)

        email_ = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email='no-reply@estavos.com',
            to=recipient_list,
            headers={'Reply-To': email}
        )
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return


class TalentForm(forms.ModelForm):
    """ """
    class Meta:
        model = Talent
        exclude = ['added', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'birth': forms.DateInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }


