from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string

import bleach
import jinja2
from caching.base import CachingManager, CachingMixin
from product_details import product_details


ENGLISH_LANGUAGE_CHOICES = sorted(
    [(key.lower(), u'{0} ({1})'.format(key, value['English']))
     for key, value in product_details.languages.items()]
)


class ModelBase(models.Model):
    """Common functions that models across the app will need."""
    class Meta:
        abstract = True


class LocaleField(models.CharField):
    description = ('CharField with locale settings specific to Affiliates '
                   'defaults.')

    def __init__(self, max_length=32, default=settings.LANGUAGE_CODE,
                 choices=ENGLISH_LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)


class NewsItem(CachingMixin, models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    html = models.TextField()
    visible = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = CachingManager()

    # Whitelisted tags allowed to be used in the HTML.
    ALLOWED_TAGS = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'dl', 'dt', 'em', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'i', 'img', 'li', 'ol', 'p', 'strong', 'ul']

    # Whitelisted attributes allowed to be used in HTML tags.
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'rel', 'class'],
        'abbr': ['title'],
        'acronym': ['title'],
        'img': ['src', 'alt', 'title'],
    }

    def render(self, locale=None):
        """Render this NewsItem as safe HTML."""
        html = self.html
        title = self.title
        if locale:
            try:
                translation = self.newsitemtranslation_set.get(locale=locale.lower())
                title = translation.title
                html = translation.html
            except NewsItemTranslation.DoesNotExist:
                pass  # Stick with the English version.

        cleaned_html = bleach.clean(html, tags=self.ALLOWED_TAGS,
                                    attributes=self.ALLOWED_ATTRIBUTES)
        rendered_html = render_to_string('base/newsitem.html', {
            'title': title,
            'html': cleaned_html
        })

        return jinja2.Markup(rendered_html)

    def __unicode__(self):
        return self.title


class NewsItemTranslation(CachingMixin, models.Model):
    newsitem = models.ForeignKey(NewsItem)
    locale = LocaleField()
    title = models.CharField(max_length=255)
    html = models.TextField()

    objects = CachingManager()

    class Meta:
        unique_together = ('newsitem', 'locale')

    def __unicode__(self):
        return self.title


# South introspection rules for LocaleField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^affiliates\.base\.models\.LocaleField'])
