from contextlib import nested
from time import time

from django.test.client import Client

from factory import Factory, SubFactory, Sequence
from mock import patch

from facebook import models
from facebook.auth import login as fb_login
from shared.tokens import TokenGenerator
from users.tests import UserFactory


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
        ctx = nested(patch('django.test.client.authenticate'),
                     patch('django.test.client.login', fb_login))
        with ctx as (authenticate, unused):
            authenticate.return_value = fb_user
            return super(FacebookAuthClient, self).login()


class FacebookUserFactory(Factory):
    FACTORY_FOR = models.FacebookUser
    id = Sequence(lambda n: 'test%s' % n)


class FacebookAccountLinkFactory(Factory):
    FACTORY_FOR = models.FacebookAccountLink
    facebook_user = SubFactory(FacebookUserFactory)
    affiliates_user = SubFactory(UserFactory)


class FacebookBannerFactory(Factory):
    FACTORY_FOR = models.FacebookBanner
    name = Sequence(lambda n: 'test%s' % n)
    image = Sequence(lambda n: 'non-existant-path')


class FacebookBannerLocaleFactory(Factory):
    FACTORY_FOR = models.FacebookBannerLocale
    banner = SubFactory(FacebookBannerFactory)


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
