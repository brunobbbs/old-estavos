#-*- coding: utf-8 -*-

from django.contrib import admin

from galeria.models import Gallery, Image


class ImagesInline(admin.TabularInline):
    model = Image
    extra = 2


class ImageAdmin(admin.ModelAdmin):
    """ """
    pass


class GalleryAdmin(admin.ModelAdmin):
    """ """
    list_display = ('title', 'description', 'count_images')
    filter_horizontal = ('images', )


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
