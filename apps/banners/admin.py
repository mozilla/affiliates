from django.contrib import admin

from funfactory.admin import site
from funfactory.urlresolvers import reverse

from badges.admin import BadgeLocaleAdminForm
from banners.models import Banner, BannerImage, BannerInstance


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 0


class BannerAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    inlines = [BannerImageInline]
    form = BadgeLocaleAdminForm
site.register(Banner, BannerAdmin)


class BannerImageAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    list_display = ('banner', 'color', 'size', 'locale', 'image')
    list_editable = ('color', 'image')
    list_filter = ('banner', 'color', 'locale')
site.register(BannerImage, BannerImageAdmin)


class BannerInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('clicks', 'created')
    list_display = ('badge', 'user_display_name', 'image', 'clicks')
    list_filter = ('badge', 'image')
    search_fields = ('badge', 'user')

    def user_display_name(self, instance):
        user = instance.user
        url = reverse('admin:auth_user_change', args=[user.id])
        return '<a href="%s">%s</a>' % (url, user.userprofile.display_name)
    user_display_name.allow_tags = True

site.register(BannerInstance, BannerInstanceAdmin)
