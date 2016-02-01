# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives


def mail_confirmed_inscription(name, email, status):
    if status == 'paid':
        message = u'''Olá {0}, tudo bem?
        Sua inscrição foi confirmada.
        Você poderá checar a lista de atletas inscritos a qualquer momento em nosso site. (estavos.com)
        O torneio acontecerá no dia 06 de Dezembro de 2015 no SESI de Taguatinga
        (QNF 24 Área Especial - Taguatinga Norte - 72125-740)
        Se tiver qualquer dúvida, não deixe de entrar em contato: contato@estavos.com.
        Atenciosamente,
        Bruno Barbosa - Academia ESTAVOS
        '''.format(name, "http://estavos.com/contato/")

        html_message = u'''
        <p>Olá {0}, tudo bem?</p>
        <p>Sua inscrição foi confirmada</p>
        <p>Você poderá <a href="{2}">checar a lista de atletas inscritos</a> a qualquer momento em nosso site.</p>
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
            subject=u"Festival de Xadrez da Família - Inscrição confirmada",
            body=message,
            from_email='no-reply@estavos.com',
            to=recipient_list,
            headers={'Reply-To': "contato@estavos.com"}
        )
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return
    return