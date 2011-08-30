from django.db import models

from badges.models import ModelBase


class NewsItemManager(models.Manager):
    def current(self):
        """
        Return the latest enabled news item. Return None if none are found.
        """
        try:
            return (NewsItem.objects.filter(enabled=True).order_by('-created')
                    .get())
        except NewsItem.DoesNotExist:
            return None


class NewsItem(ModelBase):
    """Small news blurbs that appear across the site."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, verbose_name=u'Title')
    content = models.TextField(verbose_name=u'Content')
    enabled = models.BooleanField(verbose_name=u'Show on site')

    objects = NewsItemManager()

    def __unicode__(self):
        return self.title
