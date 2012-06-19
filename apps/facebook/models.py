from django.contrib.auth.models import User
from django.db import models

from facebook.managers import FacebookUserManager
from shared.models import ModelBase


class FacebookUser(ModelBase):
    """Stores information about a user from the Facebook app."""
    user_id = models.CharField(max_length=128, unique=True)
    affiliates_user = models.ForeignKey(User, null=True)

    objects = FacebookUserManager()
