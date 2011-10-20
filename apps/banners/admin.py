from django.contrib import admin

from funfactory.admin import site
from banners.models import Banner, BannerImage, BannerInstance


class BannerAdmin(admin.ModelAdmin):
    pass
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    list_display = ('banner', 'color', 'size', 'locale', 'image')
    list_editable = ('color', 'image')
    list_filter = ('banner', 'color', 'locale')
site.register(BannerImage, BannerImageAdmin)


class BannerInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('clicks', 'created')
    list_display = ('badge', 'user', 'image', 'clicks')
    list_filter = ('badge', 'image')
    search_fields = ('badge', 'user')
site.register(BannerInstance, BannerInstanceAdmin)
