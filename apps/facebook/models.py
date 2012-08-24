import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from caching.base import CachingMixin
from funfactory.urlresolvers import reverse

from facebook.managers import FacebookAccountLinkManager, FacebookUserManager
from facebook.utils import current_hour
from shared.models import LocaleField, ModelBase
from shared.storage import OverwritingStorage
from shared.utils import absolutify


class FacebookUser(CachingMixin, ModelBase):
    """Represent a user of the Facebook app."""
    id = models.CharField(max_length=128, primary_key=True)
    leaderboard_position = models.IntegerField(default=-1)  # Max Int
    total_clicks = models.IntegerField(default=0)

    # Personal info from Facebook
    full_name = models.CharField(max_length=256, blank=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    locale = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=16, blank=True,
                               choices=settings.COUNTRIES.items())

    objects = FacebookUserManager()

    @property
    def is_new(self):
        """A user is new if they have yet to create a Facebook banner."""
        return not self.banner_instance_set.exists()

    @property
    def account_link(self):
        """
        When the account link doesn't exist, Django raises a DoesNotExist error.
        We'd rather have this behave like a ForeignKey and return None.
        See https://code.djangoproject.com/ticket/10227 for details.
        """
        try:
            return self._account_link
        except FacebookAccountLink.DoesNotExist:
            return None

    @property
    def is_linked(self):
        return self.account_link and self.account_link.is_active

    @property
    def picture_url(self):
        return 'https://graph.facebook.com/%s/picture?type=square' % self.id

    # The next few methods and properties are useful for pretending to be a real
    # Django user object.

    @property
    def is_active(self):
        """Assume Facebook users are always active... for now."""
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


class AnonymousFacebookUser(object):
    """
    Represent an anonymous user of the Facebook app.

    The primary use of this class is to implement a similar API as FacebookUser
    so that code in the Facebook app can perform checks like is_linked
    regardless of whether the user is logged in or not.
    """
    is_new = False
    account_link = None
    is_linked = False
    is_active = False

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return True


class FacebookAccountLink(CachingMixin, ModelBase):
    """Represents the link between a FacebookUser and normal User account."""
    facebook_user = models.OneToOneField(FacebookUser, unique=True,
                                         related_name='_account_link')
    affiliates_user = models.ForeignKey(User, related_name='account_links')
    activation_code = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=False)

    objects = FacebookAccountLinkManager()

    @property
    def activation_link(self):
        return absolutify(reverse('facebook.links.activate',
                                  args=[self.activation_code]))

    def generate_token_state(self):
        """
        Generate a string for use in generating an activation token. This string
        should change post-activation.
        """
        return unicode(self.id) + 'active' if self.is_active else 'inactive'


def fb_banner_rename(instance, filename):
    """Determine the filename for FacebookBanner images."""
    extension = os.path.splitext(filename)[1]
    new_filename = '{0}{1}'.format(slugify(instance.name), extension)
    return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)


class FacebookBanner(ModelBase):
    """A banner that users can customize and share on Facebook."""
    name = models.CharField(max_length=255, default='Banner', unique=True,
                            verbose_name='Banner name')
    image = models.ImageField(upload_to=fb_banner_rename,
                              storage=OverwritingStorage(),
                              max_length=settings.MAX_FILEPATH_LENGTH)


class FacebookBannerLocale(ModelBase):
    banner = models.ForeignKey(FacebookBanner, related_name='locale_set')
    locale = LocaleField()


def fb_instance_image_rename(instance, filename):
    """Determine the filename for a custom FacebookBannerInstance image."""
    extension = os.path.splitext(filename)[1]
    new_filename = '%s_%s%s' % (instance.user.id, instance.banner.id, extension)
    return os.path.join(settings.FACEBOOK_BANNER_INSTANCE_IMAGE_PATH,
                        new_filename)


class FacebookBannerInstance(ModelBase):
    """Specific instance of a customized banner."""
    user = models.ForeignKey(FacebookUser, related_name='banner_instance_set')
    banner = models.ForeignKey(FacebookBanner, default=None)
    text = models.CharField(max_length=256)
    can_be_an_ad = models.BooleanField(default=False)
    custom_image = models.ImageField(blank=True,
                                     default='',
                                     upload_to=fb_instance_image_rename,
                                     storage=OverwritingStorage(),
                                     max_length=settings.MAX_FILEPATH_LENGTH)

    created = models.DateTimeField(default=datetime.now)
    total_clicks = models.IntegerField(default=0)
    processed = models.BooleanField(default=False)

    @property
    def link(self):
        return absolutify(reverse('facebook.banners.link', args=[self.id]))

    @property
    def image(self):
        if self.custom_image:
            return self.custom_image
        else:
            return self.banner.image


class FacebookClickStats(ModelBase):
    banner_instance = models.ForeignKey(FacebookBannerInstance)
    hour = models.DateTimeField(default=current_hour)
    clicks = models.IntegerField(default=0)
