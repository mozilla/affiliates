from django.contrib import admin

from affiliates.admin import site
from banners.models import Banner, BannerImage, BannerInstance


class BannerAdmin(admin.ModelAdmin):
    pass
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    pass
site.register(BannerImage, BannerImageAdmin)


class BannerInstanceAdmin(admin.ModelAdmin):
    pass
site.register(BannerInstance, BannerInstanceAdmin)
