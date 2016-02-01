from django.db import models
from datetime import date


class CompetitorsResponsibleQuerySet(models.QuerySet):

    def confirmed(self):
        return self.prefetch_related('competitors').filter(paid=True)


class CompetitorQuerySet(models.QuerySet):

    def categoria(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(1997, 1, 1)
        ).order_by('school', 'name', 'birth')

    def sub_7(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(2008, 1, 1)
        ).order_by('school', 'name', 'birth')

    def sub_9(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(2006, 1, 1),
            birth__lte=date(2007, 12, 31),
        ).order_by('school', 'name', 'birth')

    def sub_12(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(2003, 1, 1),
            birth__lte=date(2005, 12, 31),
        ).order_by('school', 'name', 'birth')

    def sub_15(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(2000, 1, 1),
            birth__lte=date(2002, 12, 31),
        ).order_by('school', 'name', 'birth')

    def sub_18(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=1,
            birth__gte=date(1997, 1, 1),
            birth__lte=date(1999, 12, 31),
        ).order_by('school', 'name', 'birth')

    def absoluto(self):
        return self.select_related('responsible').filter(
            responsible__paid=True,
            responsible__competition__pk=2
        ).order_by('name', 'school')
