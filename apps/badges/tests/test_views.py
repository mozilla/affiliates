import json

from django.core.urlresolvers import reverse

from nose.tools import eq_
from test_utils import TestCase

from badges.tests import LocalizingClient


class TestMonthStatsAjax(TestCase):
    client_class = LocalizingClient
    fixtures = ['badge_instance']

    def test_basic(self):
        self.client.login(username='testuser43', password='asdfasdf')
        response = self.client.post(reverse('badges.ajax.stats'),
                                    {'month': 7, 'year': 2011})

        eq_(200, response.status_code)
        eq_('application/json', response['Content-Type'])

        data = json.loads(response.content)
        eq_(data['user_total'], '10')
        eq_(data['site_avg'], '5')
