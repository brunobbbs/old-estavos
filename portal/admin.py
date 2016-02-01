# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *


class ServiceAdmin(admin.ModelAdmin):
    """ """
    prepopulated_fields = {'slug': ('title', )}


class QuoteAdmin(admin.ModelAdmin):
    """ """
    list_display = ('author', 'quote')


class TestimonialAdmin(admin.ModelAdmin):
    """ """
    list_display = ('title', 'author', 'complementary')


class CourseLeadAdmin(admin.ModelAdmin):
    """ """
    list_display = ('name', 'email', 'phone')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(AboutUs)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Talent)
admin.site.register(CourseLead, CourseLeadAdmin)
