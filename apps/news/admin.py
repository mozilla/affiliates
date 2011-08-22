from django.contrib import admin

from funfactory.admin import site
from news.models import NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'created', 'modified')
    list_editable = ('enabled',)
site.register(NewsItem, NewsItemAdmin)
