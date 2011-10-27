from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

from caching.base import CachingManager, CachingMixin

from shared.models import LocaleField, ModelBase, MultiTableParentModel


# Cache keys
CACHE_CLICKS_AVG = 'clicks_avg_%s_%s'
CACHE_CLICKS_USERPERIOD_TOTAL = 'clicks_userperiod_total_%s_%s_%s'
CACHE_CLICKS_USER_TOTAL = 'clicks_user_total_%s'
CACHE_TOP_USERS = 'top_users'


class Category(CachingMixin, ModelBase):
    """Top-level category that contains sub-categories."""
    name = models.CharField(max_length=255)

    objects = CachingManager()

    def __unicode__(self):
        return self.name


class SubcategoryManager(CachingManager):
    def in_locale(self, locale):
        return self.filter(badge__badgelocale__locale=locale).distinct()


class Subcategory(CachingMixin, ModelBase):
    """Second-level category that contains badges."""
    parent = models.ForeignKey(Category)
    name = models.CharField(max_length=255)
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    max_length=settings.MAX_FILEPATH_LENGTH)

    objects = SubcategoryManager()

    def __unicode__(self):
        return self.name


class Badge(CachingMixin, MultiTableParentModel):
    """
    Parent model for any banner, text link, or other item that users will put
    on their website as an affiliate link.
    """
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory)
    preview_img = models.ImageField(upload_to=settings.BADGE_PREVIEW_PATH,
                                    max_length=settings.MAX_FILEPATH_LENGTH)
    href = models.URLField(verbose_name=u'URL to redirect to')

    objects = CachingManager()

    def customize_url(self):
        return self.child().customize_url()

    def __unicode__(self):
        return self.name


class BadgeLocale(CachingMixin, ModelBase):
    """Stores the locales that a banner is available in."""
    locale = LocaleField()
    badge = models.ForeignKey(Badge)

    objects = CachingManager()

    def __unicode__(self):
        return '%s in %s' % (self.badge, self.locale)


class BadgeInstanceManager(CachingManager):
    def for_user_by_category(self, user):
        results = defaultdict(list)

        instances = BadgeInstance.objects.filter(user=user)
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
    clicks = models.PositiveIntegerField(default=0)

    objects = BadgeInstanceManager()

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
        results = (BadgeInstance.objects.filter(user=user)
                   .aggregate(models.Sum('clicks')))
        return results['clicks__sum'] or 0

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
