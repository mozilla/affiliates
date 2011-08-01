from django.db import models

import settings


class ModelBase(models.Model):
    """For future use if needed"""
    class Meta:
        abstract = True


class LocaleField(models.CharField):
    """CharField with locale settings specific to Affiliates defaults."""
    def __init__(self, max_length=7, default=settings.LANGUAGE_CODE,
                 choices=settings.LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)
