from django.contrib import admin, auth
from django.utils.safestring import mark_safe

from affiliates.base.admin import admin_site
from affiliates.links.models import Link
from affiliates.users.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    fields = ('display_name', 'website', 'bio')


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0
    max_num = 0
    fields = ('banner', 'banner_variation', 'destination', 'link_clicks')
    readonly_fields = ('banner', 'banner_variation', 'destination', 'link_clicks')

    def banner(self, link):
        return link.banner

    def banner_variation(self, link):
        return mark_safe(link.banner_variation)

    def link_clicks(self, link):
        return link.link_clicks


class UserAdmin(auth.admin.UserAdmin):
    """Configuration for the user admin pages."""
    list_display = ['display_name', 'email', 'is_staff', 'username']
    search_fields = ['email', 'userprofile__display_name', 'username']
    inlines = [UserProfileInline, LinkInline]


admin_site.register(auth.models.User, UserAdmin)
