from nose.tools import eq_
from test_utils import TestCase

from badges.models import Badge, Subcategory
from banners.models import Banner


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
