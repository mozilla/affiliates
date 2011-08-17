from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from banners.models import Banner


class BannerTests(TestCase):
    fixtures = ['banners']

    @patch.object(settings, 'PORT', 80)
    @patch.object(settings, 'DOMAIN', 'badge.mo.com')
    def test_image_url_dict(self):
        banner = Banner.objects.get(pk=1)
        results = banner.image_url_dict()

        eq_(results['120x240']['Green'], self.banner_url('120x240arrow_g.png'))
        eq_(results['120x240']['Blue'], self.banner_url('120x240arrow_b.png'))
        eq_(results['300x250']['Green'],
            self.banner_url('mobile_dl_300x250_grn_1.png'))

    def banner_url(self, filename):
        return 'http://badge.mo.com/media/uploads/banners/%s' % filename

    def test_image_size_color_dict(self):
        banner = Banner.objects.get(pk=1)
        results = banner.image_size_color_dict()

        eq_(results['120x240'], ['Blue', 'Green', 'Red'])
        eq_(results['300x250'], ['Green', 'Red'])
