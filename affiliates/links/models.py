from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum


class Link(models.Model):
    """Affiliate link that banners link to."""
    user = models.ForeignKey(User)
    destination = models.URLField(max_length=255)
    html = models.TextField()

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

    def get_absolute_url(self):
        return reverse('links.detail', args=[self.pk])


class DataPoint(models.Model):
    """Stores the metric totals for a specific day, for a link."""
    link = models.ForeignKey(Link)
    date = models.DateField()

    link_clicks = models.PositiveIntegerField(default=0)
    firefox_downloads = models.PositiveIntegerField(default=0)
    firefox_os_referrals = models.PositiveIntegerField(default=0)


class LeaderboardStanding(models.Model):
    """Ranking in a leaderboard for a specific metric."""
    ranking = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    value = models.PositiveIntegerField(default=0)
    metric = models.CharField(max_length=255, choices=(
        ('link_clicks', 'Link Clicks'),
        ('firefox_downloads', 'Firefox Downloads'),
        ('firefox_os_referrals', ('Firefox OS Referrals'))
    ))
