import json

from django.core.urlresolvers import reverse

from nose.tools import eq_
from test_utils import TestCase

from badges.tests import LocalizingClient


class TestMonthStatsAjax(TestCase):
    client_class = LocalizingClient
    fixtures = ['badge_instance']

    def test_basic(self):
        self.client.login(username='testuser43@asdf.asdf', password='asdfasdf')
        response = self.client.post(reverse('badges.ajax.stats'),
                                    {'month': 7, 'year': 2011})

        eq_(200, response.status_code)
        eq_('application/json', response['Content-Type'])

        data = json.loads(response.content)
        eq_(data['user_total'], '12')
        eq_(data['site_avg'], '6')


class TestHome(TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def test_redirect_logged_in(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        response = self.client.get(reverse('home'))

        eq_(response.status_code, 302)


class TestNewBadgeStep2(TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def test_no_subcategory_404(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')

        path = reverse('badges.new.step2', kwargs={'subcategory_pk': 9999})
        response = self.client.get(path)

        eq_(response.status_code, 404)


class TestMyBadges(TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def test_new_user_redirect(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        response = self.client.get(reverse('my_badges'))
        eq_(response.status_code, 302)
