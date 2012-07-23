from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from nose.tools import eq_

from facebook.auth import SESSION_KEY
from facebook.middleware import FacebookAuthenticationMiddleware
from facebook.tests import FacebookUserFactory
from shared.tests import TestCase


class FacebookAuthenticationMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()
        self.auth_middleware = FacebookAuthenticationMiddleware()

    def request(self, url='/'):
        request = self.factory.get('/')
        self.session_middleware.process_request(request)
        return request

    def test_no_session(self):
        """
        If there is no authenticated  session, there should be no fb_user
        attribute on the request after the middleware runs.
        """
        request = self.request()
        self.auth_middleware.process_request(request)
        eq_(getattr(request, 'fb_user', None), None)

    def test_no_matching_user(self):
        """
        If an invalid user id is given in the session, there should be no
        fb_user attribute on the request after the middleware runs.
        """
        request = self.request()
        request.session[SESSION_KEY] = 9999
        self.auth_middleware.process_request(request)
        eq_(getattr(request, 'fb_user', None), None)

    def test_user_found(self):
        """
        If there is an authenticated session with an existing user, the
        specified user should be available via the fb_user attribute.
        """
        request = self.request()
        user = FacebookUserFactory.create()
        request.session[SESSION_KEY] = user.id
        self.auth_middleware.process_request(request)
        eq_(getattr(request, 'fb_user', None), user)
