from django.contrib import admin

from news.models import NewsItem
from shared.admin import BaseModelAdmin


class NewsItemAdmin(BaseModelAdmin):
    list_display = ('title', 'enabled', 'created', 'modified')
    list_editable = ('enabled',)
admin.site.register(NewsItem, NewsItemAdmin)
