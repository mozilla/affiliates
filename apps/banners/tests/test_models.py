from mock import patch
from nose.tools import ok_

from banners.models import BannerInstance
from shared.tests import TestCase


class BannerInstanceTests(TestCase):
    fixtures = ['banners']

    @patch('banners.models._locale')
    def test_code_alt_translated(self, _locale):
        """
        Test that the alt text for a banner instance is localized to the
        instance's locale.
        """
        banner = BannerInstance.objects.get(pk=2)
        banner.code

        ok_(_locale.called_once_with('Fast Forward', 'en-us'))
