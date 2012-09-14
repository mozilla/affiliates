from datetime import datetime

from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from facebook.auth import login
from facebook.models import FacebookUser
from facebook.tests import FacebookUserFactory
from shared.tests import TestCase


session_middleware = SessionMiddleware()


@patch.object(FacebookUser.objects, 'update_user_info')
class LoginTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def request(self, url='/'):
        """
        Create a mock request object.
        """
        request = self.factory.get(url)
        session_middleware.process_request(request)
        return request

    def test_flush_session(self, update_user_info):
        """
        If a previous login session is found and logging in as a different user,
        flush the previous session.
        """
        request = self.request()
        user1 = FacebookUserFactory()
        login(request, user1)

        request.session['somedata'] = 1
        user2 = FacebookUserFactory()
        login(request, user2)
        ok_(not 'somedata' in request.session)

    def test_new_session_key(self, update_user_info):
        """
        If there is an existing, unauthenticated session, change the session
        key on the request.
        """
        request = self.request()
        old_key = request.session.session_key
        user = FacebookUserFactory()

        login(request, user)
        ok_(request.session.session_key != old_key)

    def test_request_user(self, update_user_info):
        """
        After a user is logged in, the user attribute should be set on the
        request object.
        """
        request = self.request()
        user = FacebookUserFactory()
        login(request, user)
        eq_(request.user, user)

    def test_new_user_update_user_info_called(self, update_user_info):
        """Ensure that update_user_info is called on a successful login."""
        request = self.request()
        user = FacebookUserFactory(last_login=None)
        login(request, user)
        update_user_info.assert_called_once_with(user)

    @patch('facebook.auth.update_user_info')
    def test_old_user_task_scheduled(self, update_task, update_method):
        """
        If the user logging in isn't new, use the asynchronous task to update
        their info instead of the normal method.
        """
        request = self.request()
        user = FacebookUserFactory()
        login(request, user)
        update_task.delay.assert_called_once_with(user.id)
        ok_(not update_method.called)

    @patch('facebook.auth.datetime')
    def test_last_login_attribute(self, mock_datetime, update_user_info):
        """
        During the login process, the last_login attribute on the user must be
        set to the current datetime.
        """
        mock_datetime.now.return_value = datetime(2012, 1, 1)
        request = self.request()
        user = FacebookUserFactory.create(last_login=datetime(2000, 1, 1))
        login(request, user)

        user = FacebookUser.objects.get(id=user.id)
        eq_(user.last_login, datetime(2012, 1, 1))
