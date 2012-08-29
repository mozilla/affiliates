from django.conf import settings

from mock import patch
from nose.tools import eq_

from facebook.models import fb_banner_rename, fb_banner_thumbnail_rename
from facebook.tests import FacebookBannerFactory
from shared.tests import TestCase


@patch.object(settings, 'FACEBOOK_BANNER_IMAGE_PATH', 'simple/path/')
class FacebookBannerRenameTest(TestCase):
    def test_fb_banner_rename(self):
        banner = FacebookBannerFactory.create(name='Test banner')
        filename = fb_banner_rename(banner, 'test.png')
        eq_(filename, 'simple/path/test-banner.png')

    def test_fb_banner_thumbnail_rename(self):
        banner = FacebookBannerFactory.create(name='Test banner')
        filename = fb_banner_thumbnail_rename(banner, 'test.png')
        eq_(filename, 'simple/path/thumb_test-banner.png')
