from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from shared.utils import absolutify, redirect


@patch.object(settings, 'SITE_ID', 1)
class TestAbsolutify(TestCase):
    fixtures = ['sites']

    def test_basic(self):
        url = absolutify('/some/url')
        eq_(url, 'http://badge.mo.com/some/url')

    def test_https(self):
        url = absolutify('/some/url', https=True)
        eq_(url, 'https://badge.mo.com/some/url')

    def test_cdn(self):
        with patch.object(settings, 'CDN_DOMAIN', None):
            url = absolutify('/some/url', cdn=True)
            eq_(url, 'http://badge.mo.com/some/url')

        with patch.object(settings, 'CDN_DOMAIN', 'cdn.badge.mo.com'):
            url = absolutify('/some/url', cdn=True)
            eq_(url, 'http://cdn.badge.mo.com/some/url')


class TestRedirect(TestCase):
    urls = 'shared.tests.urls'

    def test_basic(self):
        response = redirect('mock_view')
        eq_(response.status_code, 302)
        eq_(response['Location'], '/en-US/mock_view')

    def test_permanent(self):
        response = redirect('mock_view', permanent=True)
        eq_(response.status_code, 301)
        eq_(response['Location'], '/en-US/mock_view')
