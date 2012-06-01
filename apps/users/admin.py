from django.contrib import admin
from django.contrib.auth.models import User

from funfactory.admin import site

from users.models import UserProfile
from shared.admin import BaseModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    fieldsets = (
        (None, {'fields': ('display_name',)}),
        ('Address', {'fields': ('name', 'address_1', 'address_2', 'city',
                                'state', 'postal_code', 'country')}),
    )


class UserAdmin(BaseModelAdmin):
    list_display = ('user_displayname', 'email', 'is_active', 'last_login',
                    'date_joined')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'is_active')}),
    )
    inlines = [UserProfileInline]
    search_fields = ('userprofile__display_name', 'email')

    def user_displayname(self, instance):
        return instance.userprofile.display_name

site.register(User, UserAdmin)
