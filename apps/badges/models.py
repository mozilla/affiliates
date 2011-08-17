from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from product_details import product_details
from tower import ugettext_lazy as _lazy


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


class Category(ModelBase):
    """Top-level category that contains sub-categories."""
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))

    def __unicode__(self):
        return self.name


class Subcategory(ModelBase):
    """Second-level category that contains badges."""
    parent = models.ForeignKey(Category)
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    verbose_name=_lazy(u'category preview'),
                                    max_length=settings.MAX_FILEPATH_LENGTH)

    def __unicode__(self):
        return self.name


class BadgeManager(models.Manager):
    BADGE_BANNER = 'Banner'

    def from_badge_str(self, badge_str):
        """
        Return the class and primary key corresponding to the given badge
        string.
        """
        badge_type, pk = badge_str.split(';')
        if badge_type == self.BADGE_BANNER:
            from banners.models import Banner
            return (Banner, pk)

        return None

    def all_from_subcategory(self, subcategory):
        """
        Retrieves all the badges for the given subcategory.

        Useful for the future when there will be more than on type of badge.
        """
        return subcategory.banner_set.all()


class Badge(ModelBase):
    """
    Abstract model for any banner, text link, or other item that users will put
    on their website as an affiliate link.
    """
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))
    subcategory = models.ForeignKey(Subcategory)
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    verbose_name=_lazy(u'badge preview'),
                                    max_length=settings.MAX_FILEPATH_LENGTH)
    objects = BadgeManager()


    # Subclasses should override this with the string name for the view for
    # customizing badges.
    customize_view = None

    class Meta:
        abstract = True

    def to_badge_str(self):
        """Return string representing this badge, including its class."""
        return '%s;%s' % (self.__class__.__name__, self.pk)

    def __unicode__(self):
        return self.name


class BadgeInstance(ModelBase):
    """Single user-created instance of a badge."""
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'Badge for %s' % self.user
