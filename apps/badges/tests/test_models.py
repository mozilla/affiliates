from datetime import datetime

from django.contrib.auth.models import User

from nose.tools import eq_
from test_utils import TestCase

from badges.models import BadgeInstance, ClickStats, Subcategory


class FakeDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


class SubcategoryTests(TestCase):
    fixtures = ['subcategories']

    def test_in_locale(self):
        """Test that in_locale returns all subcategories with badges available
        in the given locale.
        """
        results = Subcategory.objects.in_locale('en-us')
        eq_(len(results), 2)

        results = Subcategory.objects.in_locale('es')
        eq_(len(results), 1)


class BadgeInstanceTests(TestCase):
    fixtures = ['badge_instance']

    def setUp(self):
        self.badge_instance = BadgeInstance.objects.get(pk=2)

    def test_for_user_by_category(self):
        user = User.objects.get(pk=5)
        categories = BadgeInstance.objects.for_user_by_category(user)
        expect = {'Firefox': [self.badge_instance]}
        eq_(categories, expect)


class ClickStatsTests(TestCase):
    fixtures = ['badge_instance']

    def test_total_for_user_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user(user), 23)

    def test_total_for_user_period_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user_period(user, 7, 2011), 12)

    def test_average_for_period_basic(self):
        eq_(ClickStats.objects.average_for_period(7, 2011), 6)
        eq_(ClickStats.objects.average_for_period(8, 2011), 11)
