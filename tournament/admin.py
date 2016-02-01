#-*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Tournament, Competitor, CompetitorsResponsible


class CompetitorsInline(admin.TabularInline):

    model = Competitor


class ResponsiblesInline(admin.TabularInline):

    model = CompetitorsResponsible


class TournamentAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'date')
    inlines = (ResponsiblesInline, )


class CompetitorResponsibleResource(resources.ModelResource):

    class Meta:
        model = CompetitorsResponsible


class CompetitorResponsibleAdmin(ImportExportModelAdmin):

    def inscription_date_display(self, obj):
        return obj.inscription_date.strftime('%d/%m/%Y - %H:%M:%S')
    inscription_date_display.short_description = u'Inscrição'

    def competitors_count(self, obj):
        return obj.competitors.count()
    competitors_count.short_description = 'Atletas inscritos'

    resource_class = CompetitorResponsibleResource

    list_display = ('name', 'email', 'inscription_date_display', 'competition', 'competitors_count', 'paid')
    list_filter = ('paid', 'competition', 'payment_type')
    inlines = (CompetitorsInline, )


class CompetitorResource(resources.ModelResource):

    class Meta:
        model = Competitor


class CompetitorAdmin(ImportExportModelAdmin):

    def confirmed(self, obj):
        return obj.responsible.paid
    confirmed.boolean = True
    confirmed.short_description = 'Confirmado'

    def birth_display(self, obj):
        return obj.birth.strftime('%d/%m/%Y')
    birth_display.short_description = 'Data de nascimento'

    def competition_display(self, obj):
        return obj.responsible.competition
    competition_display.short_description = 'Competição'

    resource_class = CompetitorResource

    list_display = ('name', 'birth_display', 'school', 'competition_display', 'category_name', 'confirmed')
    list_filter = ('responsible__competition', 'responsible__paid')

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(CompetitorsResponsible, CompetitorResponsibleAdmin)
admin.site.register(Competitor, CompetitorAdmin)
