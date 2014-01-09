from datetime import datetime, timedelta

from django.contrib import admin
from django.db import models

from form_utils.widgets import ImageWidget

from affiliates.facebook.models import (FacebookBanner, FacebookBannerInstance,
                             FacebookBannerLocale, FacebookClickStats,
                             FacebookUser)
from affiliates.shared.admin import admin_site, BaseModelAdmin
from affiliates.stats.options import ModelStats


class FacebookBannerLocaleInline(admin.TabularInline):
    model = FacebookBannerLocale
    extra = 0
    fields = ('locale', 'image', 'thumbnail')
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}


class FacebookBannerAdmin(BaseModelAdmin):
    list_display = ('name', 'link', '_alt_text')
    search_fields = ('name', 'link', '_alt_text')
    fieldsets = (
        (None, {'fields': ('name', 'link', '_alt_text')}),
        ('Images', {'fields': ('image', 'thumbnail')}),
    )
    inlines = [FacebookBannerLocaleInline]
admin_site.register(FacebookBanner, FacebookBannerAdmin)


class FacebookBannerInstanceAdmin(BaseModelAdmin):
    list_display = ('text', 'banner', 'user', 'locale', 'can_be_an_ad',
                    'use_profile_image', 'created', 'total_clicks',
                    'review_status')
    search_fields = ('text', 'banner__name', 'user__full_name', 'id')
    list_filter = ('banner', 'created', 'processed', 'review_status',
                   'total_clicks')
    readonly_fields = ('created', 'total_clicks')
    fieldsets = (
        (None, {
            'fields': ('user', 'banner', 'locale', 'text', 'created',
                       'total_clicks')
        }),
        ('Ad Review', {
            'fields': ('can_be_an_ad', 'review_status', 'custom_image')
        }),
        ('Advanced', {
            'fields': ('processed',),
            'classes': ('collapse',)
        }),
    )

    def use_profile_image(self, instance):
        return bool(instance.custom_image)
    use_profile_image.boolean = True
admin_site.register(FacebookBannerInstance, FacebookBannerInstanceAdmin)


class FacebookUserAdmin(BaseModelAdmin):
    list_display = ('full_name', 'locale', 'country', 'leaderboard_position',
                    'total_clicks', 'id')
    search_fields = ('full_name', 'id')
    list_filter = ('locale', 'country')
    readonly_fields = ('full_name', 'first_name', 'last_name', 'locale',
                       'country', 'leaderboard_position', 'id', 'total_clicks')
    fieldsets = (
        (None, {
            'fields': ('full_name', 'id', 'first_name', 'last_name', 'locale',
                       'country')
        }),
        ('Leaderboard', {'fields': ('leaderboard_position', 'total_clicks')}),
    )
admin_site.register(FacebookUser, FacebookUserAdmin)


class FacebookBannerInstanceStats(ModelStats):
    display_name = 'FacebookBannerInstances created'
    datetime_field = 'created'
    filters = ['banner', 'user__country']
admin_site.register_stats(FacebookBannerInstance, FacebookBannerInstanceStats)


class FacebookClickStatsDisplay(ModelStats):
    display_name = 'FacebookBanner clicks'
    datetime_field = 'hour'
    filters = ['banner_instance__banner', 'banner_instance__user__country']
    default_interval = 'hours'

    def default_start(self):
        return datetime.now() - timedelta(days=7)
admin_site.register_stats(FacebookClickStats, FacebookClickStatsDisplay)


class FacebookUserStats(ModelStats):
    display_name = "App authorizations"
    datetime_field = 'created'
    filters = ['country']
    default_interval = 'days'

    def default_start(self):
        return datetime.now() - timedelta(days=7)
admin_site.register_stats(FacebookUser, FacebookUserStats)
