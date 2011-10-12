from collections import defaultdict
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

from caching.base import CachingManager, CachingMixin
from tower import ugettext as _, ugettext_lazy as _lazy

from shared.utils import unicode_choice_sorted


LANGUAGE_CHOICES = unicode_choice_sorted(settings.LANGUAGES.items())


# Cache keys
CACHE_CLICKS_AVG = 'clicks_avg_%s_%s'
CACHE_CLICKS_USERPERIOD_TOTAL = 'clicks_userperiod_total_%s_%s_%s'
CACHE_CLICKS_USER_TOTAL = 'clicks_user_total_%s'
CACHE_TOP_USERS = 'top_users'
CACHE_FOR_USER_BY_CATEGORY = 'for_user_by_category_%s'


class ModelBase(models.Model):
    """Common functions that models across the app will need."""

    def __init__(self, *args, **kwargs):
        super(ModelBase, self).__init__(*args, **kwargs)

        # Cache localized attributes
        self._localized_attrs = {}

    def localized(self, attr):
        """Return a localized version of the requested attribute."""
        if attr not in self._localized_attrs:
            self._localized_attrs[attr] = _(getattr(self, attr))

        return self._localized_attrs[attr]

    class Meta:
        abstract = True


class MultiTableParentModel(ModelBase):
    """
    Provides boilerplate for models that will be the parent in a multi-table
    inheritence relationship.
    """
    child_type = models.CharField(max_length=255, editable=False)

    def save(self, *args, **kwargs):
        """Set type to our classname on save."""
        if not self.child_type:
            self.child_type = self.__class__.__name__.lower()
        return super(MultiTableParentModel, self).save(*args, **kwargs)

    def child(self):
        """Return this instance's child model instance."""
        return getattr(self, self.child_type)

    class Meta:
        abstract = True


class LocaleField(models.CharField):
    description = ('CharField with locale settings specific to Affiliates '
                   'defaults.')

    def __init__(self, max_length=32, default=settings.LANGUAGE_CODE,
                 choices=LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)


class Category(CachingMixin, ModelBase):
    """Top-level category that contains sub-categories."""
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))

    objects = CachingManager()

    def __unicode__(self):
        return self.name


class Subcategory(CachingMixin, ModelBase):
    """Second-level category that contains badges."""
    parent = models.ForeignKey(Category)
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    verbose_name=_lazy(u'category preview'),
                                    max_length=settings.MAX_FILEPATH_LENGTH)

    objects = CachingManager()

    def __unicode__(self):
        return self.name


class Badge(CachingMixin, MultiTableParentModel):
    """
    Parent model for any banner, text link, or other item that users will put
    on their website as an affiliate link.
    """
    name = models.CharField(max_length=255, verbose_name=_lazy(u'name'))
    subcategory = models.ForeignKey(Subcategory)
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    verbose_name=_lazy(u'badge preview'),
                                    max_length=settings.MAX_FILEPATH_LENGTH)
    href = models.URLField(verbose_name=u'URL to redirect to')

    objects = CachingManager()

    def customize_url(self):
        return self.child().customize_url()

    def __unicode__(self):
        return self.name


class BadgeInstanceManager(CachingManager):
    def for_user_by_category(self, user):
        results = defaultdict(list)

        key = CACHE_FOR_USER_BY_CATEGORY % user.id
        instances = cache.get(key)
        if instances is None:
            instances = (BadgeInstance.objects
                         .filter(user=user)
                         .annotate(downloads=models.Sum('clickstats__clicks')))
            cache.set(key, list(instances))

        for instance in instances:
            results[instance.badge.subcategory.parent.name].append(instance)

        return results


class BadgeInstance(CachingMixin, MultiTableParentModel):
    """
    Single instance of a badge that a user has created and sent clicks to.
    """
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)

    objects = BadgeInstanceManager()

    def add_click(self):
        """Increment the click count for this badge instance."""
        now = datetime.now()

        stats, created = self.clickstats_set.get_or_create(month=now.month,
                                                           year=now.year)
        stats.clicks = models.F('clicks') + 1
        stats.save()

    def render(self):
        """Return the HTML to display this BadgeInstance."""
        return self.child().render()

    def details_template(self):
        """
        Return the path for the template used to render details about
        this badgeinstance on the my_banners page. Returns None if there
        is no template.
        """
        return getattr(self.child(), 'details_template', None)


class ClickStatsManager(models.Manager):
    def total_for_user(self, user):
        """Return the total number of clicks found for the given user."""
        key = CACHE_CLICKS_USER_TOTAL % user.id
        total = cache.get(key)
        if total is None:
            total = self._total(badge_instance__user=user)
            cache.set(key, total)

        return total

    def total_for_user_period(self, user, month, year):
        """
        Return the total number of clicks found for the given user and month.
        """
        key = CACHE_CLICKS_USERPERIOD_TOTAL % (user.id, month, year)
        total = cache.get(key)
        if total is None:
            total = self._total(badge_instance__user=user, month=month,
                                year=year)
            cache.set(key, total)

        return total

    def _total(self, **kwargs):
        """Return the total number of clicks for the given filters."""
        clickstats = self.filter(**kwargs)
        results = clickstats.aggregate(models.Sum('clicks'))
        return results['clicks__sum'] or 0

    def average_for_period(self, month, year):
        """Return the average number of clicks for the given period."""
        key = CACHE_CLICKS_AVG % (month, year)
        average = cache.get(key)
        if average is None:
            clicks_sum = models.Sum('badgeinstance__clickstats__clicks')
            results = (User.objects
                       .filter(badgeinstance__clickstats__month__exact=month,
                               badgeinstance__clickstats__year__exact=year)
                       .annotate(clicks=clicks_sum)
                       .aggregate(models.Avg('clicks')))

            # Average is sometimes None, so substitute 0
            average = results['clicks__avg'] or 0

            # Remove decimal
            average = int(average)
            cache.set(key, average)

        return average


class ClickStats(ModelBase):
    """Tracks historical data for an affiliate's referrals."""
    badge_instance = models.ForeignKey(BadgeInstance)

    month = models.IntegerField(choices=[(k, k) for k in range(1, 13)])
    year = models.IntegerField()
    clicks = models.IntegerField(default=0)

    objects = ClickStatsManager()
    class Meta:
        unique_together = ('badge_instance', 'month', 'year')


class LeaderboardManager(CachingManager):
    def top_users(self, count):
        leaderboard = cache.get(CACHE_TOP_USERS)
        if leaderboard is None:
            leaderboard = (self.select_related('user', 'user__userprofile')
                           .order_by('ranking')[:count])
            cache.set(CACHE_TOP_USERS, list(leaderboard))
        return leaderboard


class Leaderboard(CachingMixin, ModelBase):
    """Stores a user's standing in the leaderboard."""
    ranking = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    clicks = models.PositiveIntegerField()

    objects = LeaderboardManager()
