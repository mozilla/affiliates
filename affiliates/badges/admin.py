from datetime import datetime, timedelta

from django.contrib import admin

from affiliates.badges.models import BadgePreview, Category, ClickStats, Subcategory
from affiliates.shared.admin import admin_site, BaseModelAdmin
from affiliates.stats.options import ModelStats


class CategoryAdmin(BaseModelAdmin):
    change_list_template = 'smuggler/change_list.html'
admin_site.register(Category, CategoryAdmin)


class SubcategoryAdmin(BaseModelAdmin):
    change_list_template = 'smuggler/change_list.html'
admin_site.register(Subcategory, SubcategoryAdmin)


class BadgePreviewInline(admin.TabularInline):
    """
    Inline editor that lets you add localized preview images directly from a
    badge's admin page.
    """
    model = BadgePreview
    extra = 0


class ClickStatsDisplay(ModelStats):
    display_name = 'Banner clicks'
    datetime_field = 'datetime'
    filters = ['badge_instance__badge']
    default_interval = 'months'

    def default_start(self):
        return datetime.now() - timedelta(days=100)
admin_site.register_stats(ClickStats, ClickStatsDisplay)
