from django.db import models

from badges.models import MultiTableParentModel


class MultiTableParent(MultiTableParentModel):
    pass


class MultiTableChild(MultiTableParent):
    some_value = models.IntegerField()
