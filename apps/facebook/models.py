import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify

import jinja2
from caching.base import CachingManager, CachingMixin
from funfactory.urlresolvers import reverse
from tower import ugettext_lazy as _lazy

from facebook import managers
from facebook.utils import current_hour
from shared.models import LocaleField, ModelBase
from shared.storage import OverwritingStorage
from shared.utils import absolutify, get_object_or_none


class FacebookUser(CachingMixin, ModelBase):
    """Represent a user of the Facebook app."""
    id = models.CharField(max_length=128, primary_key=True,
                          verbose_name='Facebook User ID')
    leaderboard_position = models.IntegerField(default=-1)  # Max Int
    total_clicks = models.IntegerField(default=0)

    # Personal info from Facebook
    full_name = models.CharField(max_length=256, blank=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    locale = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=16, blank=True,
                               choices=settings.COUNTRIES.items())

    created = models.DateTimeField(default=datetime.now)
    last_login = models.DateTimeField(default=None, blank=True, null=True)

    objects = managers.FacebookUserManager()

    @property
    def is_new(self):
        """A user is new if they have yet to create a Facebook banner."""
        return not self.banner_instance_set.filter(processed=True).exists()

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

    def __unicode__(self):
        return self.full_name

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

    objects = managers.FacebookAccountLinkManager()

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


def _generate_banner_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return '{0}{1}'.format(slugify(instance.name), extension)


def fb_banner_rename(instance, filename):
    """Determine the filename for FacebookBanner images."""
    new_filename = _generate_banner_filename(instance, filename)
    return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)


def fb_banner_thumbnail_rename(instance, filename):
    new_filename = 'thumb_%s' % _generate_banner_filename(instance, filename)
    return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)


class FacebookBanner(CachingMixin, ModelBase):
    """A banner that users can customize and share on Facebook."""
    name = models.CharField(max_length=255, default='Banner', unique=True,
                            verbose_name='Banner name')
    _alt_text = models.CharField(max_length=256, blank=True, default='',
                                 verbose_name='Image Alt Text')
    link = models.URLField(default=settings.FACEBOOK_DOWNLOAD_URL)
    image = models.ImageField(upload_to=fb_banner_rename,
                              storage=OverwritingStorage(),
                              max_length=settings.MAX_FILEPATH_LENGTH)
    thumbnail = models.ImageField(upload_to=fb_banner_thumbnail_rename,
                                  storage=OverwritingStorage(),
                                  max_length=settings.MAX_FILEPATH_LENGTH)

    objects = managers.FacebookBannerManager()

    @property
    def alt_text(self):
        return _lazy(self._alt_text) if self._alt_text != '' else ''

    def _attr_for_locale(self, attr, locale):
        """
        Return an attribute's value on a locale associated with this banner. If
        the attribute is empty or no locale is found, return the attribute on
        this banner instead.
        """
        banner_locale = get_object_or_none(FacebookBannerLocale, banner=self,
                                           locale=locale)
        if banner_locale is None:
            # Try just the language code.
            lang = locale.split('-')[0]
            banner_locale = get_object_or_none(FacebookBannerLocale,
                                               banner=self, locale=lang)

        if banner_locale is None or not getattr(banner_locale, attr, None):
            return getattr(self, attr)
        else:
            return getattr(banner_locale, attr)

    def image_for_locale(self, locale):
        """
        Return the image field for the request locale. Defaults to the banner's
        image if the locale isn't found.
        """
        return self._attr_for_locale('image', locale)

    def thumbnail_for_locale(self, locale):
        """
        Return the thumbnail field for the request locale. Defaults to the
        banner's thumbnail if the locale isn't found.
        """
        return self._attr_for_locale('thumbnail', locale)

    def __unicode__(self):
        return self.name


class FacebookBannerLocale(CachingMixin, ModelBase):
    banner = models.ForeignKey(FacebookBanner, related_name='locale_set')
    locale = LocaleField()

    def _file_rename(instance, filename):
        extension = os.path.splitext(filename)[1]
        return '{0}.{1}{2}'.format(slugify(instance.banner.name),
                                   instance.locale, extension)

    def _image_rename(instance, filename):
        new_filename = instance._file_rename(filename)
        return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)

    def _thumbnail_rename(instance, filename):
        new_filename = 'thumb_{0}'.format(instance._file_rename(filename))
        return os.path.join(settings.FACEBOOK_BANNER_IMAGE_PATH, new_filename)

    image = models.ImageField(default='', blank=True, upload_to=_image_rename,
                              storage=OverwritingStorage(),
                              max_length=settings.MAX_FILEPATH_LENGTH)
    thumbnail = models.ImageField(default='', blank=True,
                                  upload_to=_thumbnail_rename,
                                  storage=OverwritingStorage(),
                                  max_length=settings.MAX_FILEPATH_LENGTH)


def fb_instance_image_rename(instance, filename):
    """Determine the filename for a custom FacebookBannerInstance image."""
    extension = os.path.splitext(filename)[1]
    new_filename = '%s_%s%s' % (instance.user.id, instance.id, extension)
    return os.path.join(settings.FACEBOOK_BANNER_INSTANCE_IMAGE_PATH,
                        new_filename)


class FacebookBannerInstance(CachingMixin, ModelBase):
    """Specific instance of a customized banner."""
    user = models.ForeignKey(FacebookUser, related_name='banner_instance_set')
    banner = models.ForeignKey(FacebookBanner, default=None)
    locale = LocaleField(default='en-us')
    text = models.CharField(max_length=90)
    can_be_an_ad = models.BooleanField(default=False)
    custom_image = models.ImageField(blank=True,
                                     default='',
                                     upload_to=fb_instance_image_rename,
                                     storage=OverwritingStorage(),
                                     max_length=settings.MAX_FILEPATH_LENGTH)

    created = models.DateTimeField(default=datetime.now)
    total_clicks = models.IntegerField(default=0)
    total_clicks.total_clicks_goal = True

    processed = models.BooleanField(default=False)

    UNREVIEWED = 0
    PASSED = 1
    FAILED = 2
    REVIEW_CHOICES = ((UNREVIEWED, 'Unreviewed'), (PASSED, 'Passed'),
                      (FAILED, 'Failed'),)
    review_status = models.SmallIntegerField(choices=REVIEW_CHOICES, default=0)

    objects = CachingManager()

    @property
    def link(self):
        return absolutify(reverse('facebook.banners.link', args=[self.id]))

    @property
    def image(self):
        if self.custom_image:
            return self.custom_image
        else:
            return self.banner.image_for_locale(self.locale)

    def __unicode__(self):
        return u'%s: %s' % (self.banner, self.text)


@receiver(models.signals.pre_save, sender=FacebookBannerInstance)
def notify_ad_approval(sender, instance, **kwargs):
    """Notify the user when their banner instance passes review."""
    # Don't bother if the banner hasn't passed review yet.
    if instance.review_status != FacebookBannerInstance.PASSED:
        return

    # Don't bother if this instance is new.
    old_instance = get_object_or_none(FacebookBannerInstance, id=instance.id)
    if old_instance is None:
        return

    # Bother if the review status is changing.
    if old_instance.review_status != instance.review_status:
        # String is stored in apps/facebook/templates/facebook/strings.html
        # for localization.
        AppNotification.objects.create(user=instance.user,
                                       message='banner_approved')


class FacebookClickStats(CachingMixin, ModelBase):
    banner_instance = models.ForeignKey(FacebookBannerInstance)
    hour = models.DateTimeField(default=current_hour)
    clicks = models.IntegerField(default=0)

    objects = managers.FacebookClickStatsManager()


class AppNotification(CachingMixin, ModelBase):
    """
    Small message shown to users when they next log in.

    A formatting argument can be specified to insert into the string after
    localization via string.format.
    """
    MESSAGES = {
        'banner_clicks_1': _lazy("Way to go! You've had {0} clicks on your "
                                 "Firefox banner."),
        'banner_clicks_2': _lazy("Amazing! You've had {0} clicks on your "
                                 "Firefox banner. Thanks for spreading the "
                                 "word."),
        'banner_clicks_ad': _lazy("Wow! Your banner has {0} clicks! It's ready "
                                  "to grow up and become a Firefox ad."),
        'banner_approved': _lazy('Congratulations! Your Firefox banner has now '
                                 'become a Facebook ad!')
    }

    user = models.ForeignKey(FacebookUser)
    message = models.CharField(max_length=255, choices=MESSAGES.items())
    format_argument = models.CharField(max_length=255, blank=True)

    objects = CachingManager()

    @property
    def formatted_message(self):
        """Return the message with the format_argument applied."""
        return self.get_message_display().format(self.format_argument)

    def mark_as_read(self):
        """Remove this notification after it is displayed."""
        self.delete()

    def __unicode__(self):
        return u'<{0}>: {1}'.format(self.user, self.formatted_message)
