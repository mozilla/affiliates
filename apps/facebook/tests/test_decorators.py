from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_

from facebook.auth import login as fb_login
from facebook.decorators import fb_login_required
from facebook.models import FacebookUser
from facebook.tests import FacebookUserFactory
from shared.tests import TestCase


@fb_login_required
def view(request):
    return True


class FBLoginRequiredTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware()
        self.auth_middleware = AuthenticationMiddleware()

    def request(self, url='/'):
        """
        Create a mock request object.
        """
        request = self.factory.get(url)
        self.session_middleware.process_request(request)
        self.auth_middleware.process_request(request)
        return request

    def test_no_auth(self):
        """
        If the user has not been authed, return a redirect to the home page.
        """
        request = self.request()
        with self.activate('en-US'):
            response = view(request)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'home')

    def test_django_auth(self):
        """
        If the user has authed via normal django mechanisms, return a redirect.
        """
        request = self.request()
        User.objects.create_user('test@example.com', 'test@example.com',
                                 'asdf1234')
        user = authenticate(username='test@example.com', password='asdf1234')
        django_login(request, user)

        response = view(request)
        eq_(response.status_code, 302)

    @patch.object(FacebookUser.objects, 'update_user_info')
    def test_facebook_auth(self, update_user_info):
        """
        If the user has authed via the Facebook auth mechanism, execute the
        view.
        """
        request = self.request()
        user = FacebookUserFactory()
        fb_login(request, user)

        response = view(request)
        eq_(response, True)
