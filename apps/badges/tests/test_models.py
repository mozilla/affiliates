from django.core import management

import tower
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import Badge, Category, Subcategory
from banners.models import Banner


class ModelBaseTests(TestCase):
    def setUp(self):
        # Ensure xx locale is compiled
        management.call_command('compilemessages', locale='xx')

        tower.activate('xx')

    def tearDown(self):
        tower.deactivate_all()

    def localized_basic_test(self):
        # Category inherits from ModelBase
        c = Category.objects.create(name='TestString')

        eq_(c.localized('name'), 'TranslatedTestString')

    def localized_cache_test(self):
        c = Category.objects.create(name='TestString')
        ok_('name' not in c._localized_attrs)

        c.localized('name')
        ok_('name' in c._localized_attrs)


class BadgeManagerTests(TestCase):
    fixtures = ['banners']

    def test_all_from_subcategory(self):
        subcat = Subcategory.objects.get(pk=1)
        banner = Banner.objects.get(pk=1)

        banners = Badge.objects.all_from_subcategory(subcat)
        eq_(list(banners), [banner])

    def test_from_badge_str(self):
        eq_(Badge.objects.from_badge_str('Banner;1'), (Banner, '1'))
        eq_(Badge.objects.from_badge_str('HoneyBadger;4'), None)


class BadgeTests(TestCase):
    fixtures = ['banners']

    def test_to_badge_str(self):
        banner = Banner.objects.get(pk=1)
        eq_(banner.to_badge_str(), 'Banner;1')
