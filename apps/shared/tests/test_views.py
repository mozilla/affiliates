from funfactory.urlresolvers import reverse
from nose.tools import eq_

from shared.tests import TestCase


class TestHome(TestCase):
    fixtures = ['registered_users']

    def test_redirect_logged_in(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        with self.activate('en-US'):
            response = self.client.get(reverse('home'))
        eq_(response.status_code, 302)
