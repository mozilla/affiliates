from funfactory.admin import site

from news.models import NewsItem
from shared.admin import BaseModelAdmin


class NewsItemAdmin(BaseModelAdmin):
    list_display = ('title', 'enabled', 'created', 'modified')
    list_editable = ('enabled',)
site.register(NewsItem, NewsItemAdmin)
