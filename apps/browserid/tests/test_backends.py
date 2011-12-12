from django.contrib.auth.models import User

from funfactory.urlresolvers import reverse
from nose.tools import eq_, ok_

from browserid.backends import BrowserIDSessionBackend
from browserid.tests import mock_browserid
from shared.tests import SessionRequestFactory, TestCase


class BrowserIDSessionBackendTests(TestCase):
    fixtures = ['registered_users']

    def setUp(self):
        self.backend = BrowserIDSessionBackend()
        self.factory = SessionRequestFactory()

    def _auth(self, email, assertion='asdf'):
        request = self.factory.get(reverse('home'))
        with mock_browserid(email):
            return self.backend.authenticate(request, assertion)

    def test_invalid_assertion(self):
        """Return None if the assertion is invalid."""
        result = self._auth(None)
        eq_(result, None)

    def test_invalid_user(self):
        """Return None if the user does not exist."""
        result = self._auth('honey@badger.com')
        eq_(result, None)

    def test_valid_user(self):
        """Return the User object if a user exists."""
        result = self._auth('mkelly@mozilla.com')
        ok_(isinstance(result, User))
        eq_(result.email, 'mkelly@mozilla.com')
