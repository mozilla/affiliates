from django.db.models import Sum

from nose.tools import eq_
from test_utils import TestCase

from badges.models import BadgeInstance
from banners.tasks import add_click


class AddClickTests(TestCase):
    fixtures = ['banners']

    def setUp(self):
        self.badge_instance = BadgeInstance.objects.get(pk=2)

    def _click(self):
        banner_instance = self.badge_instance.child()
        add_click(self.badge_instance.user.id, banner_instance.badge.id,
                  banner_instance.image.id)

    def test_basic(self):
        old_clicks = (self.badge_instance.clickstats_set
                      .aggregate(Sum('clicks'))['clicks__sum'])

        self._click()
        new_clicks = (self.badge_instance.clickstats_set
                      .aggregate(Sum('clicks'))['clicks__sum'])
        eq_(old_clicks + 1, new_clicks)

    def test_normalized_clicks(self):
        old_clicks = self.badge_instance.clicks
        self._click()

        new_clicks = BadgeInstance.objects.get(pk=2).clicks
        eq_(old_clicks + 1, new_clicks)
