from django.contrib import admin

from funfactory.admin import site

from badges.models import BadgeInstance, BadgePreview, Category, Subcategory
from shared.admin import BaseModelAdmin
from stats.admin import ModelStats


class CategoryAdmin(BaseModelAdmin):
    change_list_template = 'smuggler/change_list.html'
site.register(Category, CategoryAdmin)


class SubcategoryAdmin(BaseModelAdmin):
    change_list_template = 'smuggler/change_list.html'
site.register(Subcategory, SubcategoryAdmin)


class BadgePreviewInline(admin.TabularInline):
    """
    Inline editor that lets you add localized preview images directly from a
    badge's admin page.
    """
    model = BadgePreview
    extra = 0


class BadgeInstanceStats(ModelStats):
    display_name = 'BadgeInstances created'
    datetime_field = 'created'
site.register_stats(BadgeInstance, BadgeInstanceStats)
