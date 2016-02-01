from django.contrib import admin

from partner.models import Partner


class PartnerAdmin(admin.ModelAdmin):
    """docstring for PartnerAdmin"""
    list_display = ['name', 'contact', 'email', 'phone']

admin.site.register(Partner, PartnerAdmin)
