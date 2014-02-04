from django.db import models

from affiliates.base.models import ModelBase, MultiTableParentModel


class ModelBaseChild(ModelBase):
    name = models.CharField(max_length=255)


class MultiTableParent(MultiTableParentModel):
    pass


class MultiTableChild(MultiTableParent):
    some_value = models.IntegerField()
