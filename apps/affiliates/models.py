from django.db import models


class ModelBase(models.Model):
    """For future use if needed"""
    class Meta:
        abstract = True
