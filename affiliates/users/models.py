from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.db import models
from django.dispatch import receiver

from product_details import product_details
from tower import ugettext_lazy as _lazy

from affiliates.base.models import ModelBase


COUNTRIES = product_details.get_regions(settings.LANGUAGE_CODE).items()
COUNTRIES.append(('', '---'))  # Empty choice


@receiver(models.signals.post_save, sender=User)
def add_default_permissions(sender, **kwargs):
    """Add default set of permissions to users when they are first created."""
    if kwargs['created']:
        user = kwargs['instance']
        can_share_website = Permission.objects.get(codename='can_share_website')
        user.user_permissions.add(can_share_website)
        user.save()


class UserProfile(ModelBase):
    """
    Stores information about a user account. Created post-activation.
    Accessible via user.get_profile().
    """

    user = models.OneToOneField(User, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, blank=True,
                            verbose_name=_lazy(u'Full Name'))
    display_name = models.CharField(max_length=255,
                                    verbose_name=_lazy(u'Display name'))

    address_1 = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name=_lazy(u'Address Line 1'))
    address_2 = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name=_lazy(u'Address Line 2'))
    city = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_lazy(u'City'))
    state = models.CharField(max_length=255, blank=True, null=True,
                             verbose_name=_lazy(u'State or Province'))
    postal_code = models.CharField(max_length=32, blank=True, null=True,
                                   verbose_name=_lazy(u'ZIP or Postal Code'))
    country = models.CharField(max_length=2, choices=COUNTRIES, blank=True,
                               verbose_name=_lazy(u'Country'))

    website = models.URLField(blank=True)

    def __unicode__(self):
        return unicode(self.display_name)

    class Meta:
        permissions = (
            ('can_share_website', 'Can share website link on leaderboard'),
        )


class RegisterProfile(ModelBase):
    """Stores activation information for a user."""
    activation_key = models.CharField(max_length=40, editable=False)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u'Registration information for %s' % self.user
