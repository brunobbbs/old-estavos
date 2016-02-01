# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Permission

from core.models import Country, State


admin.site.register(Permission)
admin.site.register(Country)
admin.site.register(State)
