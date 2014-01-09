from affiliates.news.models import NewsItem
from affiliates.shared.admin import admin_site, BaseModelAdmin


class NewsItemAdmin(BaseModelAdmin):
    list_display = ('title', 'enabled', 'created', 'modified')
    list_editable = ('enabled',)
admin_site.register(NewsItem, NewsItemAdmin)
