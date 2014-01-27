from django.contrib.auth.models import User
from django.db import models

from affiliates.shared.models import LocaleImage, ModelBase, MultiTableParentModel


class Category(ModelBase):
    """Top-level category that contains sub-categories."""
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Subcategory(ModelBase):
    """Second-level category that contains badges."""
    parent = models.ForeignKey(Category)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Badge(MultiTableParentModel):
    """
    Parent model for any banner, text link, or other item that users will put
    on their website as an affiliate link.
    """
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory)
    href = models.URLField(verbose_name=u'URL to redirect to')
    displayed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class BadgePreview(LocaleImage):
    badge = models.ForeignKey(Badge)

    class Meta:
        unique_together = ('locale', 'badge')

    def __unicode__(self):
        return 'Preview: %s(%s)' % (self.badge, self.locale)


class BadgeInstance(MultiTableParentModel):
    """
    Single instance of a badge that a user has created and sent clicks to.
    """
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)
    clicks = models.PositiveIntegerField(default=0)


class ClickStats(ModelBase):
    """Tracks historical data for an affiliate's referrals."""
    badge_instance = models.ForeignKey(BadgeInstance)

    datetime = models.DateTimeField()
    clicks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('badge_instance', 'datetime')


class Leaderboard(ModelBase):
    """Stores a user's standing in the leaderboard."""
    ranking = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    clicks = models.PositiveIntegerField()
