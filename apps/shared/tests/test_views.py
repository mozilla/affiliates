from django.http import HttpResponse

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from shared.tests import TestCase


class TestHome(TestCase):
    fixtures = ['registered_users']

    def test_redirect_logged_in(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        with self.activate('en-US'):
            response = self.client.get(reverse('home'))
        eq_(response.status_code, 302)

    @patch('shared.views.browserid_home')
    def test_en_us_browserid(self, browserid_home):
        """Test that en-US users get the browserid view while others don't."""
        browserid_home.return_value = HttpResponse()

        with self.activate('fr'):
            self.client.get(reverse('home'))
        ok_(not browserid_home.called, 'browserid_home called for fr')

        with self.activate('en-US'):
            self.client.get(reverse('home'))
        ok_(browserid_home.called, 'browserid_home not called for en-US')
