from django.contrib import admin

from funfactory.admin import site
from banners.models import Banner, BannerImage


class BannerAdmin(admin.ModelAdmin):
    pass
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    pass
site.register(BannerImage, BannerImageAdmin)
