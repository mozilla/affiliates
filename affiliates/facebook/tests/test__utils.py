import base64
import hashlib
import hmac
import json

from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.translation import get_language

from nose.tools import eq_

from affiliates.facebook.tests import FACEBOOK_USER_AGENT, create_payload
from affiliates.facebook.utils import (activate_locale, decode_signed_request,
                            is_facebook_bot, modified_url_b64decode)
from affiliates.base.tests import TestCase


def modified_url_b64encode(data):
    """Encodes a string in modified bsae64 for URLs."""
    return base64.b64encode(data, '-_').rstrip('=')


class DecodeSignedRequestTests(TestCase):
    def create_signed_request(self, payload, secret):
        json_payload = json.dumps(payload)
        encoded_json = modified_url_b64encode(json_payload)

        signature = hmac.new(secret, encoded_json, hashlib.sha256).digest()
        encoded_signature = modified_url_b64encode(signature)

        return '.'.join((encoded_signature, encoded_json))

    def test_invalid_request(self):
        """If the request is invalid, return None."""
        eq_(decode_signed_request('invalid()', 'secret'), None)
        eq_(decode_signed_request('invalid().withdot', 'secret'), None)

        signature = modified_url_b64encode('secret')
        payload = modified_url_b64encode('notjson')
        eq_(decode_signed_request('.'.join((signature, payload)), 's'), None)

    def test_invalid_algorithm(self):
        """If the declared algorithm isn't supported, return None."""
        payload = create_payload(algorithm='not-supported')
        signed_request = self.create_signed_request(payload, 'secret')
        eq_(decode_signed_request(signed_request, 'secret'), None)

    def test_invalid_secret(self):
        """
        If the secret used for decoding doesn't match the secret used for
        encoding, return None.
        """
        payload = create_payload()
        signed_request = self.create_signed_request(payload, 'secret')
        eq_(decode_signed_request(signed_request, 'other_secret'), None)

    def test_valid_request(self):
        """If the signed request is valid, return the decoded payload."""
        payload = create_payload()
        signed_request = self.create_signed_request(payload, 'secret')
        eq_(decode_signed_request(signed_request, 'secret'), payload)


class ModifiedUrlB64DecodeTests(TestCase):
    def test_invalid_padding(self):
        """
        If the given string has incorrect padding, the function should add the
        needed padding and decode properly.
        """
        eq_(modified_url_b64decode('abc'), base64.b64decode('abc='))
        eq_(modified_url_b64decode('ab'), base64.b64decode('ab=='))

    def test_character_replacement(self):
        """
        The modified decoding should replace the - and _ characters with + and
        / before decoding.
        """
        eq_(modified_url_b64decode('a-b_'), base64.b64decode('a+b/'))

    def test_basic_decode(self):
        """Test that basic decoding functionality works."""
        eq_(modified_url_b64decode('UA=='), 'P')


class ActivateLocaleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(DEV=False, TEST=False, FACEBOOK_LOCALES=('en-us', 'fr'))
    def test_not_in_whitelist(self):
        """
        If the given locale is not in the whitelist, default back to en-us.
        """
        request = self.factory.get('/')
        activate_locale(request, 'de')
        eq_(request.locale, 'en-us')

    @override_settings(DEV=False, TEST=False, FACEBOOK_LOCALES=('en-us', 'de'))
    def test_language_code_in_whitelist(self):
        """If only a locale's language code is in the whitelist, use it."""
        request = self.factory.get('/')
        activate_locale(request, 'de-de')
        eq_(get_language(), 'de')
        eq_(request.locale, 'de')

    @override_settings(DEV=False, TEST=False, FACEBOOK_LOCALES=('en-us', 'fr'))
    def test_locale_in_whitelist(self):
        """If a locale is in the whitelist, use it."""
        request = self.factory.get('/')
        activate_locale(request, 'en-us')
        eq_(request.locale, 'en-us')

    @override_settings(DEV=True, TEST=False, FACEBOOK_LOCALES=('en-us', 'fr'))
    def test_dev_dont_limit_locales(self):
        """
        If settings.DEV is True, do not verify that a locale is in the
        FACEBOOK_LOCALES list.
        """
        request = self.factory.get('/')
        activate_locale(request, 'es')
        eq_(request.locale, 'es')


class IsFacebookBotTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_is_bot(self):
        request = self.factory.get('/', HTTP_USER_AGENT=FACEBOOK_USER_AGENT)
        eq_(is_facebook_bot(request), True)

    def test_is_not_a_bot(self):
        request = self.factory.get('/', HTTP_USER_AGENT='not.facebook')
        eq_(is_facebook_bot(request), False)
