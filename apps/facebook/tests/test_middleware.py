from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from nose.tools import eq_, ok_

from facebook.auth import SESSION_KEY
from facebook.middleware import FacebookAuthenticationMiddleware
from facebook.tests import FacebookUserFactory
from shared.tests import TestCase


class FacebookAuthenticationMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()
        self.django_auth_middleware = AuthenticationMiddleware()
        self.auth_middleware = FacebookAuthenticationMiddleware()

    def request(self, url='/fb'):
        request = self.factory.get(url)
        self.session_middleware.process_request(request)
        self.django_auth_middleware.process_request(request)
        return request

    def test_no_session(self):
        """
        If there is no authenticated session, the user attribute should contain
        an anonymous user.
        """
        request = self.request()
        self.auth_middleware.process_request(request)
        eq_(request.user.is_anonymous(), True)

    def test_no_matching_user(self):
        """
        If an invalid user id is given in the session, the user attribute should
        contain an anonymous user.
        """
        request = self.request()
        request.session[SESSION_KEY] = 9999
        self.auth_middleware.process_request(request)
        eq_(request.user.is_anonymous(), True)

    def test_user_found(self):
        """
        If there is an authenticated session with an existing user, the
        specified user should be available via the user attribute.
        """
        request = self.request()
        user = FacebookUserFactory.create()
        request.session[SESSION_KEY] = user.id
        self.auth_middleware.process_request(request)
        eq_(request.user, user)

    def test_user_non_fb_app(self):
        """
        If there is an authenticated session with an existing user outside of
        the app, the specified user should not be a FacebookUser.
        """
        request = self.request(url='/')
        user = FacebookUserFactory.create()
        request.session[SESSION_KEY] = user.id
        self.auth_middleware.process_request(request)
        ok_(not request.user == user)
        eq_(request.user.is_anonymous(), True)
