import base64
import hashlib
import hmac
import json

from django.conf import settings
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_

from facebook.tests import create_payload
from facebook.utils import (activate_locale, decode_signed_request,
                            modified_url_b64decode)
from shared.tests import TestCase


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

    @patch.object(settings, 'TEST', False)
    @patch.object(settings, 'FACEBOOK_LOCALES', ('en-us', 'fr'))
    def test_not_in_whitelist(self):
        """
        If the given locale is not in the whitelist, default back to en-us.
        """
        request = self.factory.get('/')
        activate_locale(request, 'de')
        eq_(request.locale, 'en-us')

    @patch.object(settings, 'TEST', False)
    @patch.object(settings, 'FACEBOOK_LOCALES', ('en-us', 'de'))
    @patch('facebook.utils.get_language', lambda: 'de-de')
    def test_language_code_in_whitelist(self):
        """If only a locale's language code is in the whitelist, use it."""
        request = self.factory.get('/')
        activate_locale(request, 'de-de')
        eq_(request.locale, 'de-de')

    @patch.object(settings, 'TEST', False)
    @patch.object(settings, 'FACEBOOK_LOCALES', ('en-us', 'fr'))
    @patch('facebook.utils.get_language', lambda: 'en-us')
    def test_locale_in_whitelist(self):
        """If a locale is in the whitelist, use it."""
        request = self.factory.get('/')
        activate_locale(request, 'en-us')
        eq_(request.locale, 'en-us')

    @patch.object(settings, 'TEST', True)
    @patch.object(settings, 'FACEBOOK_LOCALES', ('en-us', 'fr'))
    @patch('facebook.utils.get_language', lambda: 'en-us')
    def test_testing_dont_set_request_locale(self):
        """If settings.TEST is True, do not set the locale on the request."""
        request = self.factory.get('/')
        activate_locale(request, 'en-us')
        eq_(getattr(request, 'locale', None), None)
