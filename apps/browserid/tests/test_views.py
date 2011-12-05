import json

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from browserid.forms import RegisterForm
from browserid.tests import mock_browserid
from browserid.views import register
from shared.tests import TestCase


@patch.object(settings, 'SITE_URL', 'http://testserver')
class VerifyTests(TestCase):
    fixtures = ['registered_users']

    def _verify(self, assertion=None):
        if assertion is not None:
            data = {'assertion': assertion}
        else:
            data = {}

        with self.activate('en-US'):
            return self.client.post(reverse('browserid.verify'),
                                        data=data)

    def test_no_assertion(self):
        """Test that an HTTP 400 is sent if an assertion isn't given."""
        response = self._verify()
        eq_(response.status_code, 400)

    @mock_browserid(None)
    def test_invalid_assert(self):
        """Test that an invalid assert gets an HTTP 403."""
        response = self._verify('asdf')
        eq_(response.status_code, 403)

    @mock_browserid('not@registered.com')
    def test_not_registered(self):
        """Test for proper response with unregistered user."""
        response = self._verify('asdf')
        eq_(response.status_code, 200)
        eq_(json.loads(response.content), {'registered': False})

    @mock_browserid('mkelly@mozilla.com')
    def test_registered(self):
        """Test for proper response with registered user."""
        response = self._verify('asdf')
        eq_(response.status_code, 200)

        data = json.loads(response.content)
        eq_(data['registered'], True)
        ok_('redirect' in data, 'Response does not specify a redirect.')


class RegisterTests(TestCase):
    fixtures = ['registered_users']

    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()

    def _register(self, data={}):
        default_data = {
            'display_name': 'TestUser',
            'assertion': 'asdf',
            'agreement': True
        }
        default_data.update(data)

        with self.activate('en-US'):
            request = self.factory.post(reverse('home'), data=default_data)

            # Init session because middleware isn't run during tests
            self.session_middleware.process_request(request)

        response = register(request, RegisterForm(default_data))

        return {'request': request, 'response': response}

    def test_invalid_form(self):
        """Return None if the form isn't valid."""
        result = self._register({'agreement': False})
        eq_(result['response'], None)

    @mock_browserid(None)
    def test_invalid_assert(self):
        """Return None if the assertion is invalid."""
        result = self._register()
        eq_(result['response'], None)

    @mock_browserid('mkelly@mozilla.com')
    def test_registered(self):
        """
        Return redirect and do not register if the user is already registered.
        """
        result = self._register();
        eq_(result['response'].status_code, 302)
        eq_(User.objects.filter(email='mkelly@mozilla.com').count(), 1)

    @mock_browserid('honey@badger.com')
    def test_new_user(self):
        """Return redirect and register if user is new."""
        result = self._register()
        eq_(result['response'].status_code, 302)
        ok_('_auth_user_id' in result['request'].session,
            'New user was not logged in.')
