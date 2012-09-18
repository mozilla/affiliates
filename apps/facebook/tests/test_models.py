from django.conf import settings

from mock import patch
from nose.tools import eq_, ok_

from facebook.models import fb_banner_rename, fb_banner_thumbnail_rename
from facebook.tests import FacebookBannerFactory, FacebookBannerLocaleFactory
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


class FacebookBannertests(TestCase):
    def test_image_for_locale_no_locale(self):
        """
        If a banner is not available in the requested locale, return the default
        image.
        """
        banner = FacebookBannerFactory.create(image='test')
        ok_(banner.image_for_locale('es').name.endswith('test'))

    def test_image_for_locale_found(self):
        """
        If the banner is available in the requested locale, return the image for
        that locale.
        """
        banner = FacebookBannerFactory.create(image='banner')
        FacebookBannerLocaleFactory.create(banner=banner, locale='pt-BR',
                                           image='locale')
        ok_(banner.image_for_locale('pt-BR').name.endswith('locale'))

    def test_image_for_locale_fallback(self):
        """
        If the banner is available in a certain language and the requested
        locale is a subset of that language that isn't available, return the
        image for the fallback language.
        """
        banner = FacebookBannerFactory.create(image='banner')
        FacebookBannerLocaleFactory.create(banner=banner, locale='de',
                                           image='locale')
        ok_(banner.image_for_locale('de-ch').name.endswith('locale'))

    def test_image_for_locale_blank_default(self):
        """
        If a banner is available in the requested locale but the image is blank,
        return the default image.
        """
        banner = FacebookBannerFactory.create(image='banner')
        FacebookBannerLocaleFactory.create(banner=banner, locale='es',
                                           image='')
        ok_(banner.image_for_locale('es').name.endswith('banner'))
