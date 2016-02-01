# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


class Menu(object):
    """
    Each class variable bellow is an user group registered on Groups table.
    The base var always appear.
    """
    base = [
        {
            'title': _(u"Início"),
            'url': 'dashboard:home',
            'permission': '',
            'icon_class': 'fa fa-home',
            'submenu': []
        },
        {
            'title': _(u"Festival de Xadrez"),
            'url': 'dashboard:home',
            'permission': '',
            'icon_class': 'fa fa-trophy',
            'submenu': [
                {
                    'title': _(u"Por categorias"),
                    'url': 'tournament:dash_list_inscription',
                    'permission': '',
                    'icon_class': 'fa fa-sitemap',
                    'submenu': []
                },
                {
                    'title': _(u"Absoluto"),
                    'url': 'tournament:dash_list_inscription',
                    'permission': '',
                    'icon_class': 'fa fa-sitemap',
                    'submenu': []
                },
            ]
        },
    ]
    cliente = []
    aluno = []
    instrutor = [
        {
            'title': _(u"ESAP"),
            'url': 'dashboard:classes',
            'permission': 'esap.view_classes',
            'icon_class': 'fa fa-delicious',
            'submenu': [
                {
                    'title': _(u"Aulas de Xadrez"),
                    'url': 'dashboard:classes',
                    'permission': 'esap.view_keyword',
                    'icon_class': 'fa fa-puzzle-piece',
                    'submenu': []
                },
                {
                    'title': _(u"Tags"),
                    'url': 'dashboard:keywords',
                    'permission': 'esap.view_keyword',
                    'icon_class': 'fa fa-tag',
                    'submenu': []
                },
                {
                    'title': _(u"Módulos"),
                    'url': 'dashboard:modules',
                    'permission': 'esap.view_module',
                    'icon_class': 'fa fa-shield',
                    'submenu': []
                },
                {
                    'title': _(u"Instrutores"),
                    'url': 'dashboard:instructors',
                    'permission': 'esap.view_instructor',
                    'icon_class': 'fa fa-slideshare',
                    'submenu': []
                },
                {
                    'title': _(u"Clientes particulares"),
                    'url': 'dashboard:particularclients',
                    'permission': 'esap.view_particularclient',
                    'icon_class': 'fa fa-male',
                    'submenu': []
                }
            ]
        },
    ]

    def __init__(self, user):
        self.user = user

    def get_groups(self):
        """ Get all user's groups and returns it on lower list format """
        user_groups = self.user.groups.all()
        groups = []
        for group in user_groups:
            groups.append(group.name.lower())
        return groups

    def filter_menu_by_perm(self, menu_item):
        """ returns only item groups that user has permission """
        menu = []
        for item in menu_item:
            if self.user.has_perm(item.get('permission')):
                menu.append(item)
        return menu

    def get_menu_items(self):
        groups = self.get_groups()
        menu = []
        menu += self.base
        for i in groups:
            item = self.filter_menu_by_perm(getattr(self, i, []))
            menu += item
        return menu

    def get(self):
        menu = {
            'menu': self.get_menu_items()
        }
        return menu
