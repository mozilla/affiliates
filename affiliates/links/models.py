from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum

from affiliates.base.utils import absolutify

class Link(models.Model):
    """Affiliate link that banners link to."""
    user = models.ForeignKey(User)
    html = models.TextField()

    banner_variation_content_type = models.ForeignKey(ContentType)
    banner_variation_id = models.PositiveIntegerField()
    banner_variation = generic.GenericForeignKey('banner_variation_content_type',
                                                 'banner_variation_id')

    # Aggregates do not include data currently stored in the DataPoint
    # model. After a retention period, DataPoint data is added to these
    # aggregate counts and removed from the database.
    aggregate_link_clicks = models.PositiveIntegerField(default=0)
    aggregate_firefox_downloads = models.PositiveIntegerField(default=0)
    aggregate_firefox_os_referrals = models.PositiveIntegerField(default=0)

    # Ids for supporting old Affiliates URLs
    legacy_banner_instance_id = models.IntegerField(default=None, null=True)
    legacy_banner_image_id = models.IntegerField(default=None, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def _get_metric_total(self, metric):
        """
        Get the sum total for a specific metric by combining data from
        the DataPoint table and the aggregate stored on this link.
        """
        datapoint_sum = self.datapoint_set.aggregate(Sum(metric))['{0}__sum'.format(metric)]
        return getattr(self, 'aggregate_{0}'.format(metric)) + (datapoint_sum or 0)

    @property
    def link_clicks(self):
        return self._get_metric_total('link_clicks')

    @property
    def firefox_downloads(self):
        return self._get_metric_total('firefox_downloads')

    @property
    def firefox_os_referrals(self):
        return self._get_metric_total('firefox_os_referrals')

    @property
    def banner(self):
        return self.banner_variation.banner if self.banner_variation else None

    @property
    def destination(self):
        return self.banner.destination

    @property
    def is_upgrade_link(self):
        from affiliates.banners.models import FirefoxUpgradeBanner
        return isinstance(self.banner, FirefoxUpgradeBanner)

    @property
    def is_image_link(self):
        from affiliates.banners.models import ImageBanner
        return isinstance(self.banner, ImageBanner)

    @property
    def is_text_link(self):
        from affiliates.banners.models import TextBanner
        return isinstance(self.banner, TextBanner)

    def preview_html(self, href):
        return self.banner.preview_html(href)

    def get_referral_url(self):
        return absolutify(reverse('links.referral', args=[self.pk]))

    def get_absolute_url(self):
        return reverse('links.detail', args=[self.pk])


class DataPoint(models.Model):
    """Stores the metric totals for a specific day, for a link."""
    link = models.ForeignKey(Link)
    date = models.DateField()

    link_clicks = models.PositiveIntegerField(default=0)
    firefox_downloads = models.PositiveIntegerField(default=0)
    firefox_os_referrals = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('link', 'date')


class LeaderboardStanding(models.Model):
    """Ranking in a leaderboard for a specific metric."""
    ranking = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    value = models.PositiveIntegerField(default=0)
    metric = models.CharField(max_length=255, choices=(
        ('link_clicks', 'Link Clicks'),
        ('firefox_downloads', 'Firefox Downloads'),
        ('firefox_os_referrals', ('Firefox OS Referrals'))
    ))

    class Meta:
        unique_together = ('ranking', 'metric')

    def __unicode__(self):
        return u'{metric}: {ranking}'.format(metric=self.metric, ranking=self.ranking)
