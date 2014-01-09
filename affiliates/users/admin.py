from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from affiliates.users.models import UserProfile
from affiliates.shared.admin import admin_site, BaseModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    fieldsets = (
        (None, {'fields': ('display_name', 'website')}),
        ('Address', {'fields': ('name', 'address_1', 'address_2', 'city',
                                'state', 'postal_code', 'country')}),
    )


class UserAdmin(BaseModelAdmin, DjangoUserAdmin):
    list_display = ('user_displayname', 'email', 'is_active', 'last_login',
                    'date_joined')
    list_filter = ('is_active',)
    inlines = [UserProfileInline]
    search_fields = ('userprofile__display_name', 'email')

    def user_displayname(self, instance):
        return instance.userprofile.display_name


admin_site.register(User, UserAdmin)
