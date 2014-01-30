from django.contrib.auth.models import User
from django.db import models


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
