from django.contrib import admin
from django.db.models import ImageField

from form_utils.widgets import ImageWidget
from mptt.admin import MPTTModelAdmin

from affiliates.banners import models
from affiliates.base.admin import admin_site, BaseModelAdmin


class CategoryModelAdmin(MPTTModelAdmin):
    pass


class ImageVariationInline(admin.TabularInline):
    model = models.ImageBannerVariation
    fields = ('color', 'locale', 'image')
    formfield_overrides = {ImageField: {'widget': ImageWidget}}
    extra = 0


class ImageBannerModelAdmin(BaseModelAdmin):
    list_display = ('name', 'category', 'destination', 'visible')
    fields = ('name', 'category', 'destination', 'visible', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('name', 'destination', 'category__name')
    inlines = (ImageVariationInline,)


class TextVariationInline(admin.TabularInline):
    model = models.TextBannerVariation
    fields = ('locale', 'text')
    extra = 0


class TextBannerModelAdmin(BaseModelAdmin):
    list_display = ('name', 'category', 'visible', 'destination')
    fields = ('name', 'category', 'visible', 'destination', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('name', 'destination', 'category__name')
    inlines = (TextVariationInline,)


admin_site.register(models.Category, CategoryModelAdmin)
admin_site.register(models.ImageBanner, ImageBannerModelAdmin)
admin_site.register(models.TextBanner, TextBannerModelAdmin)
