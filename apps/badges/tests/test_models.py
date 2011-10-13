from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Sum

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import BadgeInstance, Category, ClickStats
from badges.tests import ModelsTestCase
from badges.tests.models import MultiTableParent, MultiTableChild


class ModelBaseTests(TestCase):
    @patch('badges.models._')
    def localized_basic_test(self, _):
        # Category inherits from ModelBase
        c = Category.objects.create(name='TestString')
        c.localized('name')
        _.assert_called_with('TestString')

    def localized_cache_test(self):
        c = Category.objects.create(name='TestString')
        ok_('name' not in c._localized_attrs)

        c.localized('name')
        ok_('name' in c._localized_attrs)


class MultiTableParentModelTests(ModelsTestCase):
    apps = ['badges.tests']

    def setUp(self):
        self.child = MultiTableChild.objects.create(some_value=10)

    def test_child(self):
        parent = MultiTableParent.objects.all()[0]
        eq_(parent.child_type, 'multitablechild')
        eq_(parent.child(), self.child)


class FakeDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


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
