from django.conf import settings
from django.db import models

from product_details import product_details


LANGUAGE_CHOICES = tuple([(i, product_details.languages[i]['native']) for i in
                          settings.AFFILIATES_LANGUAGES])


class ModelBase(models.Model):
    """For future use if needed"""
    class Meta:
        abstract = True


class LocaleField(models.CharField):
    """CharField with locale settings specific to Affiliates defaults."""
    def __init__(self, max_length=7, default=settings.LANGUAGE_CODE,
                 choices=LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)
