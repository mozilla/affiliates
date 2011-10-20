import hashlib
import hmac
import random
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import get_language

from product_details import product_details
from tower import ugettext_lazy as _lazy

from badges.models import ModelBase, LocaleField
from users.utils import hash_password


COUNTRIES = product_details.get_regions(settings.LANGUAGE_CODE).items()
COUNTRIES.append(('', '---'))  # Empty choice
SHA1_RE = re.compile('^[a-f0-9]{40}$')


ACTIVATION_EMAIL_SUBJECT = _lazy('Please activate your Firefox Affiliates '
                                 'account')


# Extra User Methods
def has_created_badges(self):
    return self.badgeinstance_set.count() > 0
User.add_to_class('has_created_badges', has_created_badges)


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
                                   verbose_name=_lazy(u'Zip or Postal Code'))
    country = models.CharField(max_length=2, choices=COUNTRIES, blank=True,
                               verbose_name=_lazy(u'Country'))

    locale = LocaleField(verbose_name=_lazy(u'Locale'))

    def __unicode__(self):
        return unicode(self.display_name)


class RegisterManager(models.Manager):
    """
    Custom manager for creating registration profiles and activating them.

    Users are sent an email upon creation that contains a link with an
    activation code. This code will create their account and direct the user
    to fill out their profile information.
    """

    def create_profile(self, display_name, email, password):
        """
        Create a registration profile and return it. Also sends an
        activation email to the given email address.

        Activation keys are a hash generated from the user's email and a
        random salt.
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hmac.new(salt, email, hashlib.sha1).hexdigest()

        # get_or_create lets us replace existing profiles
        profile, created = RegisterProfile.objects.get_or_create(email=email)
        profile.display_name = display_name
        profile.activation_key = activation_key
        profile.set_password(password)
        profile.save()

        self._send_email('users/email/activation_email.html',
                         ACTIVATION_EMAIL_SUBJECT, profile)

        return profile

    def activate_profile(self, key):
        """
        Create a User and UserProfile, and deactivate the corresponding
        RegisterProfile.

        If the activation key is valid, create the User and
        UserProfile, and return the new User.

        If the key is invalid, return ``None``.
        """
        reg_profile = self.get_by_key(key)
        if reg_profile:
            # Username isn't used but is required and has silly constraints.
            # So we make one up.
            username = hashlib.sha1(reg_profile.email).hexdigest()[:30]
            user = User(username=username,
                        email=reg_profile.email,
                        password=reg_profile.password,
                        is_active=True)
            user.save()
            UserProfile.objects.create(user=user,
                                       display_name=reg_profile.display_name,
                                       locale=get_language().lower())
            reg_profile.delete()
            return user

        return None

    def get_by_key(self, key):
        """
        Validates an activation key and returns the corresponding
        RegisterProfile. If the key is invalid, return None.
        """
        # Check for a valid SHA-1 hash before hitting the DB
        if SHA1_RE.match(key):
            try:
                return self.get(activation_key=key)
            except self.model.DoesNotExist:
                pass

        return None

    def _send_email(self, template, subject, profile, **kwargs):
        """Sends an activation email to the user"""
        current_site = Site.objects.get_current()
        url = reverse('users.activate',
                     kwargs={'activation_key': profile.activation_key})
        email_kwargs = {'domain': current_site.domain,
                        'activate_url': url}
        email_kwargs.update(kwargs)
        message = render_to_string(template, email_kwargs)
        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                       [profile.email])


class RegisterProfile(ModelBase):
    """Stores activation information for a user."""
    activation_key = models.CharField(max_length=40, editable=False)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user = models.OneToOneField(User, null=True)

    objects = RegisterManager()

    def set_password(self, raw_password):
        """
        Sets the profile's password to a properly hashed password.
        """
        self.password = hash_password(raw_password)

    def __unicode__(self):
        return u'Registration information for %s' % self.user
