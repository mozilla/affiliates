from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from banners.models import Banner


@patch.object(settings, 'SITE_ID', 1)
class BannerTests(TestCase):
    fixtures = ['banners', 'sites']

    def _banner_url(self, filename, domain='badge.mo.com'):
        return 'http://%s/media/uploads/banners/%s' % (domain, filename)

    def test_banner_image_dict(self):
        banner = Banner.objects.get(pk=1)
        results = banner.banner_image_dict()

        eq_(results['120x240']['Green']['image_url'],
            self._banner_url('120x240arrow_g.png'))
        eq_(results['120x240']['Blue']['image_url'],
            self._banner_url('120x240arrow_b.png'))
        eq_(results['300x250']['Green']['image_url'],
            self._banner_url('mobile_dl_300x250_grn_1.png'))

    @patch.object(settings, 'CDN_DOMAIN', 'cdn.badge.mo.com')
    def test_banner_image_cdn(self):
        banner = Banner.objects.get(pk=1)
        results = banner.banner_image_dict()

        eq_(results['120x240']['Green']['image_url'],
            self._banner_url('120x240arrow_g.png', domain='cdn.badge.mo.com'))

    def test_image_size_color_dict(self):
        banner = Banner.objects.get(pk=1)
        results = banner.image_size_color_dict()

        eq_(results['120x240'], ['Blue', 'Green', 'Red'])
        eq_(results['300x250'], ['Green', 'Red'])
