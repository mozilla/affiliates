from django.contrib import admin

from funfactory.admin import site
from banners.models import Banner, BannerImage


class BannerAdmin(admin.ModelAdmin):
    pass
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
site.register(BannerImage, BannerImageAdmin)
