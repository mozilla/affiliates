import os
from contextlib import nested
from datetime import datetime
from os.path import abspath, dirname
from time import time

from django.test.client import Client

from factory import Factory, LazyAttribute, SubFactory, Sequence
from mock import patch

from facebook import models
from facebook.models import FacebookUser
from facebook.auth import login as fb_login
from shared.tokens import TokenGenerator
from users.tests import UserFactory


FACEBOOK_USER_AGENT = ('facebookexternalhit/1.1 (+http://www.facebook.com/'
                       'externalhit_uatext.php)')


def path(*a):
    return os.path.join(dirname(abspath(__file__)), *a)


def create_payload(user_id=None, algorithm='HMAC-SHA256', country='us',
                   locale='en_US'):
    """Creates a signed request payload with the proper structure."""
    payload = {
        'algorithm': algorithm,
        'issued_at': int(time()),
        'user': {
            'country': country,
            'locale': locale
        }
    }

    if user_id:
        payload['user_id'] = user_id
    return payload


class FacebookAuthClient(Client):
    def fb_login(self, fb_user):
        """
        Sets the Factory to appear as if it has successfully logged into a site.
        Uses the Facebook authentication mechanism.
        """
        # Instead of duplicating code, we just mock out the authentication
        # mechanisms from the test client code!
        # We also mock out update_user_info to avoid requests calls.
        ctx = nested(patch('django.test.client.authenticate'),
                     patch('django.test.client.login', fb_login),
                     patch.object(FacebookUser.objects, 'update_user_info'))
        with ctx as (authenticate, unused, unused):
            authenticate.return_value = fb_user
            return super(FacebookAuthClient, self).login()


class FacebookUserFactory(Factory):
    FACTORY_FOR = models.FacebookUser
    id = Sequence(lambda n: 'test%s' % n)
    last_login = LazyAttribute(lambda o: datetime.now())


class FacebookAccountLinkFactory(Factory):
    FACTORY_FOR = models.FacebookAccountLink
    facebook_user = SubFactory(FacebookUserFactory)
    affiliates_user = SubFactory(UserFactory)


class FacebookBannerFactory(Factory):
    FACTORY_FOR = models.FacebookBanner
    name = Sequence(lambda n: 'test%s' % n)
    image = Sequence(lambda n: 'non-existant-path')
    thumbnail = Sequence(lambda n: 'non-existant-path')


class FacebookBannerLocaleFactory(Factory):
    FACTORY_FOR = models.FacebookBannerLocale
    banner = SubFactory(FacebookBannerFactory)


class FacebookBannerInstanceFactory(Factory):
    FACTORY_FOR = models.FacebookBannerInstance
    banner = SubFactory(FacebookBannerFactory)
    user = SubFactory(FacebookUserFactory)
    text = Sequence(lambda n: 'test%s' % n)


class FacebookAccountLinkFactory(Factory):
    FACTORY_FOR = models.FacebookAccountLink
    facebook_user = SubFactory(FacebookUserFactory)
    affiliates_user = SubFactory(UserFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        link = super(FacebookAccountLinkFactory, cls)._prepare(create, **kwargs)
        if create and 'activation_code' not in kwargs.keys():
            token_generator = TokenGenerator(link.generate_token_state)
            link.activation_code = token_generator.generate_token()
            link.save()
        return link


class FacebookClickStatsFactory(Factory):
    FACTORY_FOR = models.FacebookClickStats
    banner_instance = SubFactory(FacebookBannerInstanceFactory)


class AppNotificationFactory(Factory):
    FACTORY_FOR = models.AppNotification
    user = SubFactory(FacebookUserFactory)
    message = Sequence(lambda n: 'test_{0}'.format(n))
