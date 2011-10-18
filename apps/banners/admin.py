from django.contrib import admin

from funfactory.admin import site
from banners.models import Banner, BannerImage


class BannerAdmin(admin.ModelAdmin):
    pass
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    list_display = ('banner', 'color', 'size', 'image')
    list_editable = ('color', 'image')
    list_filter = ('banner', 'color')
site.register(BannerImage, BannerImageAdmin)
