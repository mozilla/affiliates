from nose.tools import eq_, ok_
from mock import patch

from facebook.models import FacebookBannerInstance, FacebookClickStats
from facebook.tasks import add_click
from facebook.tests import FacebookBannerInstanceFactory
from shared.tests import TestCase


class AddClickTests(TestCase):
    @patch.object(FacebookClickStats.objects, 'get_or_create')
    def test_invalid_id(self, get_or_create):
        """If the given banner id is invalid, do nothing."""
        add_click(999)
        ok_(not get_or_create.called)

    def test_valid_id(self):
        """If the given banner id is valid, increment the click count."""
        banner = FacebookBannerInstanceFactory(total_clicks=0)
        add_click(banner.id)

        banner_instance = FacebookBannerInstance.objects.get(id=banner.id)
        eq_(banner_instance.total_clicks, 1)

        stats = FacebookClickStats.objects.get(banner_instance=banner_instance)
        eq_(stats.clicks, 1)
