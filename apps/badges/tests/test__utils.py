from django.conf import settings

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from badges.utils import fq_url


class FQUrlTests(TestCase):

    def setUp(self):
        super(FQUrlTests, self).setUp()
        self.site_patcher = patch('django.contrib.sites.models.Site.objects')
        site_mock = self.site_patcher.start()
        site_mock.get_current.return_value.domain = 'badge.mo.com'

        self.settings_patcher = patch.object(settings, '_wrapped')
        self.settings_mock = self.settings_patcher.start()
        self.settings_mock.SERVER_PORT = None

        self.abs_path = '/some/absolute/path'

    def tearDown(self):
        self.site_patcher.stop()
        self.settings_patcher.stop()
        super(FQUrlTests, self).tearDown()

    def test_basic(self):
        url = fq_url(self.abs_path)
        eq_('http://badge.mo.com/some/absolute/path', url)

    def test_https(self):
        url = fq_url(self.abs_path, https=True)
        eq_('https://badge.mo.com/some/absolute/path', url)

    def test_with_port(self):
        self.settings_mock.SERVER_PORT = 8000

        url = fq_url(self.abs_path)
        eq_('http://badge.mo.com:8000/some/absolute/path', url)
