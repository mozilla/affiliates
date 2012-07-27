import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from caching.base import CachingMixin

from facebook.managers import FacebookUserManager
from shared.models import LocaleField, ModelBase
from shared.storage import OverwritingStorage


class FacebookUser(CachingMixin, ModelBase):
    """Represent a user of the Facebook app."""
    id = models.CharField(max_length=128, primary_key=True)
    affiliates_user = models.ForeignKey(User, null=True)

    objects = FacebookUserManager()

    @property
    def is_new(self):
        """A user is new if they have yet to create a Facebook banner."""
        return not self.banner_instance_set.exists()

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


def fb_banner_rename(instance, filename):
    """Determine the filename for FacebookBanner images."""
    extension = os.path.splitext(filename)[1]
    new_filename = '{0}_{1}.{2}'.format(instance.id, instance.locale, extension)
    return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)


class FacebookBanner(ModelBase):
    """A banner that users can customize and share on Facebook."""
    name = models.CharField(max_length=255, default='Banner', unique=True,
                            verbose_name='Banner name')
    image = models.ImageField(upload_to=fb_banner_rename,
                              storage=OverwritingStorage(),
                              max_length=settings.MAX_FILEPATH_LENGTH)
    locale = LocaleField()


class FacebookBannerInstance(ModelBase):
    """Specific instance of a customized banner."""
    user = models.ForeignKey(FacebookUser, related_name='banner_instance_set')
    banner = models.ForeignKey(FacebookBanner)
    text = models.CharField(max_length=256)
    can_be_an_ad = models.BooleanField(default=False)

    created = models.DateTimeField(default=datetime.now)
    total_clicks = models.IntegerField()
    leaderboard_position = models.IntegerField()
