from django_browserid.tests import mock_browserid
from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from browserid.utils import SESSION_VERIFY, verify
from shared.tests import SessionRequestFactory, TestCase


class VerifyTests(TestCase):
    def setUp(self):
        self.factory = SessionRequestFactory()

    def _verify(self, assertion=None, email=None):
        with self.activate('en-US'):
            request = self.factory.get(reverse('home'))
        if email:
            request.session[SESSION_VERIFY] = self._verification(email)

        return verify(request, assertion)

    def _verification(self, email):
        return {'status': 'okay', 'email': email}

    @mock_browserid(None)
    def test_invalid_assertion(self):
        """Return None if the assertion is invalid."""
        result = self._verify('asdf')
        eq_(result, None)

    @mock_browserid('honey@badger.com')
    def test_valid_assertion(self):
        """Return verification if the assertion is valid."""
        result = self._verify('asdf')
        eq_(result['status'], 'okay')
        eq_(result['email'], 'honey@badger.com')

    @mock_browserid('honey@badger.com')
    @patch('browserid.utils.browserid_verify')
    def test_cached_verification(self, browserid_verify):
        """
        Return verification without connecting to BrowserID if verification
        is cached in session.
        """
        result = self._verify(email='honey@badger.com')
        eq_(result['status'], 'okay')
        eq_(result['email'], 'honey@badger.com')
        ok_(not browserid_verify.called, 'browserid_verify was called.')

        # Test that a non-cached call works, in case we mocked incorrectly
        result = self._verify('asdf')
        ok_(browserid_verify.called, 'browserid_verify was not called.')
