from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from shared.utils import absolutify


@patch.object(settings, 'SITE_ID', 1)
class TestAbsolutify(TestCase):
    fixtures = ['sites']

    def test_basic(self):
        url = absolutify('/some/url')
        eq_(url, 'http://badge.mo.com/some/url')

    def test_https(self):
        url = absolutify('/some/url', https=True)
        eq_(url, 'https://badge.mo.com/some/url')
