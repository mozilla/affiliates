import json

from django.conf import settings
from django.core.urlresolvers import reverse

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.tests import LocalizingClient
from banners.models import Banner, BannerImage, BannerInstance
from banners.tests import mock_size


FRENCH_LANGUAGE_URL_MAP = {'fr': 'fr'}


@patch.object(settings, 'LANGUAGE_URL_MAP', FRENCH_LANGUAGE_URL_MAP)
@patch.object(BannerImage, 'size', mock_size)
class CustomizeViewTests(TestCase):
    client_class = LocalizingClient
    fixtures = ['banners']

    def test_locale_images(self):
        self.client.login(username='testuser42@asdf.asdf', password='asdfasdf')

        url = reverse('banners.customize', kwargs={'banner_pk': 1})
        response = self.client.get('/%s%s' % ('fr', url))

        banner_images = json.loads(response.context['json_banner_images'])
        eq_(banner_images['300x250 pixels']['Red']['pk'], 5)


class LinkViewTests(TestCase):
    fixtures = ['banners']

    BANNER_ID = 1
    USER_ID = 1
    BANNER_IMG_ID = 1

    BAD_BANNER_IMG_ID = 666

    def test_basic(self):
        kwargs = {'user_id': self.USER_ID,
                  'banner_id': self.BANNER_ID,
                  'banner_img_id': self.BANNER_IMG_ID}
        url = reverse('banners.link', kwargs=kwargs)
        response = self.client.get(url)

        results = BannerInstance.objects.filter(
            user__id=self.USER_ID,
            badge__id=self.BANNER_ID,
            image__id=self.BANNER_IMG_ID)
        ok_(results.exists())

        banner = Banner.objects.get(pk=self.BANNER_ID)
        eq_(response.status_code, 302)
        eq_(response['Location'], banner.href)

    @patch.object(settings, 'DEFAULT_AFFILIATE_LINK', 'http://testlink.com')
    def test_redirect_default_on_error(self):
        kwargs = {'user_id': self.USER_ID,
                  'banner_id': self.BANNER_ID,
                  'banner_img_id': self.BAD_BANNER_IMG_ID}
        url = reverse('banners.link', kwargs=kwargs)
        response = self.client.get(url)

        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testlink.com')
