# -*- coding: utf-8 -*-

from esap.menu import Menu


def menu(request):
    menu = Menu(request.user)
    return menu.get()


def dashboard(request):
    context_vars = {
        'user': request.user,
    }
    return context_vars
