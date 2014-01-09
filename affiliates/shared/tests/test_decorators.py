from django.conf import settings

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_

from affiliates.shared.tests import TestCase


@patch.object(settings, 'LOGIN_VIEW_NAME', 'mock_login_view')
class TestLoginRequired(TestCase):
    fixtures = ['registered_users']
    urls = 'shared.tests.urls'

    def test_basic(self):
        with self.activate('en-US'):
            response = self.client.get(reverse('mock_view'))
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US/mock_login_view')

    def test_logged_in(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        with self.activate('en-US'):
            response = self.client.get(reverse('mock_view'))
        eq_(response.status_code, 200)
