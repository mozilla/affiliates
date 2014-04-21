from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver

from tower import ugettext as _

from affiliates.base.models import ModelBase
from affiliates.base.utils import get_object_or_none
from affiliates.links.models import LeaderboardStanding


# User class extensions
@property
def display_name(self):
    """Return the user's display name, or a localized default."""
    return self.userprofile.display_name or _(u'Affiliate')
User.add_to_class('display_name', display_name)


# User class extensions
def user_metric_aggregate_total(self, metric):
    return sum(getattr(link, 'aggregate_' + metric) for link in self.link_set.all())
User.add_to_class('metric_aggregate_total', user_metric_aggregate_total)

def user_metric_total(self, metric):
    return sum(getattr(link, metric) for link in self.link_set.all())
User.add_to_class('metric_total', user_metric_total)

def user_leaderboard_rank(self, metric):
    standing = get_object_or_none(LeaderboardStanding, user=self, metric=metric)
    return standing.ranking if standing else None
User.add_to_class('leaderboard_rank', user_leaderboard_rank)


@receiver(models.signals.post_save, sender=User)
def add_default_permissions(sender, **kwargs):
    """Add default set of permissions to users when they are first created."""
    if kwargs['created']:
        user = kwargs['instance']

        try:
            can_share_website = Permission.objects.get(codename='can_share_website')
        except Permission.DoesNotExist:
            # Permission will be created by migration and thus doesn't
            # need to be added now.
            return

        user.user_permissions.add(can_share_website)
        user.save()


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create a user profile when a new user is created."""
    if kwargs['created']:
        user = kwargs['instance']
        UserProfile.objects.create(user=user)


class UserProfile(ModelBase):
    """
    Stores information about a user account. Created post-activation.
    """
    user = models.OneToOneField(User, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    last_visit = models.DateField(blank=True, null=True, default=None)

    display_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.display_name)

    def get_absolute_url(self):
        return reverse('users.profile', args=(self.pk,))

    class Meta:
        permissions = (
            ('can_share_website', 'Can share website link on leaderboard'),
        )
