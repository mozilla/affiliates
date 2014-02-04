from django.conf import settings
from django.db import models

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


# South introspection rules for LocaleField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^affiliates\.base\.models\.LocaleField'])
