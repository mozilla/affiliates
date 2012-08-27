import json

from funfactory.urlresolvers import reverse
from nose.tools import eq_

from badges.models import Category
from shared.tests import TestCase


class TestMonthStatsAjax(TestCase):
    fixtures = ['badge_instance']

    def test_basic(self):
        self.client.login(username='testuser43@asdf.asdf', password='asdfasdf')

        with self.activate('en-US'):
            response = self.client.get(reverse('badges.ajax.stats',
                                                args=[7, 2011]))
        eq_(200, response.status_code)
        eq_('application/json', response['Content-Type'])

        data = json.loads(response.content)
        eq_(data['user_total'], '12')
        eq_(data['site_avg'], '6')


class TestNewBadgeStep2(TestCase):
    fixtures = ['registered_users', 'subcategories']

    def test_no_subcategory_404(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')

        with self.activate('en-US'):
            path = reverse('badges.new.step2', kwargs={'subcategory_pk': 9999})
        response = self.client.get(path)

        eq_(response.status_code, 404)

    def test_no_available_badges_404(self):
        self.client.login(username='testuser43@asdf.asdf', password='asdfasdf')

        with self.activate('en-US'):
            path = reverse('badges.new.step2', kwargs={'subcategory_pk': 13})
        response = self.client.get(path)

        eq_(response.status_code, 404)


class TestMyBadges(TestCase):
    fixtures = ['registered_users']

    def test_new_user_redirect(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        with self.activate('en-US'):
            response = self.client.get(reverse('my_badges'))
        eq_(response.status_code, 302)


class TestDisplayedBadges(TestCase):
    fixtures = ['subcategories']

    def setUp(self):
        self.client.login(username='testuser43@asdf.asdf', password='asdfasdf')

    def test_step_1(self):
        """Test that step1 doesn't display categories with no displayed badges"""
        with self.activate('en-US'):
            path = reverse('badges.new.step1')
        response = self.client.get(path)

        categories = response.context['categories']
        category = Category.objects.filter(pk=11)

        eq_(list(categories), list(category))

    def test_step_2(self):
        """Test that views for subcategories with no displayed badges return a 404"""
        with self.activate('en-US'):
            path = reverse('badges.new.step2', kwargs={'subcategory_pk': 14})
        response = self.client.get(path)

        eq_(response.status_code, 404)
