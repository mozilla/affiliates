from django.core.urlresolvers import reverse

from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.tests import LocalizingClient
from banners.models import Banner, BannerInstance


class LinkViewTests(TestCase):
    client_class = LocalizingClient
    fixtures = ['banners']

    BANNER_ID = 1
    USER_ID = 1
    BANNER_IMG_ID = 1

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
