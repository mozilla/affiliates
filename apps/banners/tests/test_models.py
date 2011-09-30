from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from banners.models import Banner, BannerImage
from banners.tests import mock_size


@patch.object(BannerImage, 'size', mock_size)
@patch.object(settings, 'SITE_ID', 1)
class BannerImageTests(TestCase):
    fixtures = ['banners', 'sites']

    def _banner_url(self, filename, domain='badge.mo.com'):
        return 'http://%s/media/uploads/banners/%s' % (domain, filename)

    def test_size_color_to_image_map(self):
        banner = Banner.objects.get(pk=1)
        results = banner.bannerimage_set.all().size_color_to_image_map()

        eq_(results['120x240 pixels']['Green']['image_url'],
            self._banner_url('120x240arrow_g.png'))
        eq_(results['120x240 pixels']['Blue']['image_url'],
            self._banner_url('120x240arrow_b.png'))
        eq_(results['300x250 pixels']['Green']['image_url'],
            self._banner_url('mobile_dl_300x250_grn_1.png'))

    @patch.object(settings, 'CDN_DOMAIN', 'cdn.badge.mo.com')
    def test_size_color_to_image_map_cdn(self):
        banner = Banner.objects.get(pk=1)
        results = banner.bannerimage_set.all().size_color_to_image_map()

        eq_(results['120x240 pixels']['Green']['image_url'],
            self._banner_url('120x240arrow_g.png', domain='cdn.badge.mo.com'))

    def test_size_to_color_map(self):
        banner = Banner.objects.get(pk=1)
        results = banner.bannerimage_set.all().size_to_color_map()

        eq_(results['120x240 pixels'], ['Blue', 'Green', 'Red'])
        eq_(results['300x250 pixels'], ['Green', 'Red'])
