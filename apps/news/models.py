from django.db import models

from badges.models import ModelBase


class NewsItem(ModelBase):
    """Small news blurbs that appear across the site."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, verbose_name=u'Title')
    content = models.TextField(verbose_name=u'Content')
