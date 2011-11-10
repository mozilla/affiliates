import json

from django.core.cache import cache
from django.core.urlresolvers import reverse

from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.tests import LocalizingClient
from badges.views import CACHE_SUBCAT_MAP
from shared.tests import model_ids


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


class TestNewBadgeStep1(TestCase):
    client_class = LocalizingClient
    fixtures = ['subcategories']

    def test_available_badges_displayed(self):
        """Test that the proper available badges are displayed."""
        self.client.login(username='testuser42@asdf.asdf', password='asdfasdf')
        response = self.client.get(reverse('badges.new.step1'))

        subcategory_map = response.context['subcategory_map']
        eq_(model_ids(subcategory_map[11]), [11, 12])
        ok_(12 not in subcategory_map, 'Empty category included in '
            'subcategory_map.')

    def test_subcategory_map_cached(self):
        """Test that the subcategory map is cached."""
        cache.clear()

        self.client.login(username='testuser42@asdf.asdf', password='asdfasdf')
        self.client.get(reverse('badges.new.step1'))

        ok_(cache.get(CACHE_SUBCAT_MAP % 'en-US', False))


class TestNewBadgeStep2(TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users', 'subcategories']

    def test_no_subcategory_404(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')

        path = reverse('badges.new.step2', kwargs={'subcategory_pk': 9999})
        response = self.client.get(path)

        eq_(response.status_code, 404)

    def test_no_available_badges_404(self):
        self.client.login(username='testuser43@asdf.asdf', password='asdfasdf')

        path = reverse('badges.new.step2', kwargs={'subcategory_pk': 12})
        response = self.client.get(path)

        eq_(response.status_code, 404)


class TestMyBadges(TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def test_new_user_redirect(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        response = self.client.get(reverse('my_badges'))
        eq_(response.status_code, 302)
