from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from mock import ANY, patch
from nose.tools import eq_, ok_

from affiliates.facebook.auth import SESSION_KEY
from affiliates.facebook.middleware import FacebookAuthenticationMiddleware
from affiliates.facebook.tests import FacebookUserFactory
from affiliates.shared.tests import TestCase


class FacebookAuthenticationMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()
        self.django_auth_middleware = AuthenticationMiddleware()
        self.auth_middleware = FacebookAuthenticationMiddleware()

    def request(self, url='/fb', locale='en-US'):
        request = self.factory.get(url)
        self.session_middleware.process_request(request)
        self.django_auth_middleware.process_request(request)
        request.META['HTTP_ACCEPT_LANGUAGE'] = locale
        return request

    @patch('affiliates.facebook.middleware.activate_locale')
    def test_no_session(self, activate_locale):
        """
        If there is no authenticated session, the user attribute should contain
        an anonymous user.
        """
        request = self.request()
        self.auth_middleware.process_request(request)
        eq_(request.user.is_anonymous(), True)

        # Check that the locale from the request was activated.
        activate_locale.assert_called_once_with(ANY, 'en-US')

    @patch('affiliates.facebook.middleware.activate_locale')
    def test_no_matching_user(self, activate_locale):
        """
        If an invalid user id is given in the session, the user attribute should
        contain an anonymous user.
        """
        request = self.request(locale='es')
        request.session[SESSION_KEY] = 9999
        self.auth_middleware.process_request(request)
        eq_(request.user.is_anonymous(), True)

        # Check that the locale from the request was activated.
        activate_locale.assert_called_once_with(ANY, 'es')

    @patch('affiliates.facebook.middleware.activate_locale')
    def test_user_found(self, activate_locale):
        """
        If there is an authenticated session with an existing user, the
        specified user should be available via the user attribute.
        """
        request = self.request()
        user = FacebookUserFactory.create(locale='fr')
        request.session[SESSION_KEY] = user.id
        self.auth_middleware.process_request(request)
        eq_(request.user, user)

        # Check that the locale from the user object was activated.
        activate_locale.assert_called_once_with(ANY, 'fr')

    @patch('affiliates.facebook.middleware.activate_locale')
    def test_user_non_fb_app(self, activate_locale):
        """
        If there is an authenticated session with an existing user outside of
        the app, the specified user should not be a FacebookUser.
        """
        request = self.request(url='/', locale='pt-BR')
        user = FacebookUserFactory.create()
        request.session[SESSION_KEY] = user.id

        self.auth_middleware.process_request(request)
        ok_(not request.user == user)
        eq_(request.user.is_anonymous(), True)

        # Check that the FB locale stuff was never called.
        eq_(activate_locale.called, False)
