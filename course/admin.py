from django.contrib import admin

from .models import Subscription, Course, Student


class SubscriptionsAdmin(admin.ModelAdmin):

    list_display = ("name", "email", "subscription_date")


admin.site.register(Subscription, SubscriptionsAdmin)
admin.site.register(Course)
admin.site.register(Student)
