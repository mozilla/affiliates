from django.db.models import Sum

from nose.tools import eq_
from test_utils import TestCase

from badges.models import BadgeInstance
from badges.utils import handle_affiliate_link


class TestHandleAffiliateLink(TestCase):
    fixtures = ['badge_instance']

    def test_basic(self):
        instance = BadgeInstance.objects.all()[0]
        old_clicks = (instance.clickstats_set
                      .aggregate(Sum('clicks'))['clicks__sum'])

        response = handle_affiliate_link(instance)
        new_clicks = (instance.clickstats_set
                      .aggregate(Sum('clicks'))['clicks__sum'])

        eq_(new_clicks, old_clicks + 1)
        eq_(response['Location'], instance.badge.href)
