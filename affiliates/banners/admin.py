from django.contrib import admin

from affiliates.badges.admin import BadgePreviewInline
from affiliates.badges.models import ClickStats
from affiliates.banners.models import Banner, BannerImage, BannerInstance
from affiliates.shared.admin import admin_site, BaseModelAdmin
from affiliates.stats.options import ModelStats


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 0


class BannerAdmin(BaseModelAdmin):
    change_list_template = 'admin/banner_change_list.html'
    inlines = [BadgePreviewInline, BannerImageInline]
    list_display = ('__unicode__', 'clicks')

    def changelist_view(self, request, extra_context={}):
        extra_context.update(total=ClickStats.objects.total())
        return super(BannerAdmin, self).changelist_view(request,
            extra_context=extra_context)

admin_site.register(Banner, BannerAdmin)


class BannerImageAdmin(BaseModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    list_display = ('banner', 'color', 'size', 'locale', 'image')
    list_editable = ('color', 'image')
    list_filter = ('banner', 'color', 'locale')
    formfield_overrides = {}
admin_site.register(BannerImage, BannerImageAdmin)


class BannerInstanceAdmin(BaseModelAdmin):
    list_display = ('badge', 'user_display_name', 'image', 'clicks')
    list_filter = ('badge', 'image')
    readonly_fields = ('clicks', 'created')
    search_fields = ('badge', 'user')

    def user_display_name(self, instance):
        return instance.user.userprofile.display_name
admin_site.register(BannerInstance, BannerInstanceAdmin)


class BannerInstanceStats(ModelStats):
    display_name = 'BannerInstances created'
    datetime_field = 'created'
    filters = ['badge', 'image__locale']
admin_site.register_stats(BannerInstance, BannerInstanceStats)
