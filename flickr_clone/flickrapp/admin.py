from django.contrib import admin
from .models import Album, Image


class AlbumAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
