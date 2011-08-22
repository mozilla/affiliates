from django.db import models

from babel.dates import format_date

from badges.models import ModelBase


class NewsItem(ModelBase):
    """Small news blurbs that appear across the site."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, verbose_name=u'Title')
    content = models.TextField(verbose_name=u'Content')
    enabled = models.BooleanField(verbose_name=u'Show on site')

    def get_date(self):
        """
        Return the modified-on date of this news item in a locale-appropriate
        format.
        """
        return format_date(self.modified, format='long')

    def __unicode__(self):
        return self.title
