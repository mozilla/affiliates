from django.contrib.admin.sites import AdminSite
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_

from shared.tests import TestCase
from stats.monkeypatches import patch as patch_admin
from stats.options import ModelStats
from stats.tests.models import TestModel


class StatsAdminTests(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        patch_admin(self.admin_site)
        self.factory = RequestFactory()

    def test_modelstats_overview_called(self):
        """Test that the overview function on the ModelStats object is called
        by the overview function on the admin site.
        """
        class TestModelStats(ModelStats):
            slug = 'unique_slug'
        self.admin_site.register_stats(TestModel, TestModelStats)

        with patch.object(TestModelStats, 'overview') as overview:
            eq_(overview.called, False)
            self.admin_site.overview(self.factory.get('/test'), 'unique_slug')
            eq_(overview.called, True)

    def test_unique_slugs(self):
        """Test that the admin site generates unique slugs for multiple
        ModelStats that have identical slugs.
        """
        class TestModelStats(ModelStats):
            slug = 'unique_slug'
        self.admin_site.register_stats(TestModel, TestModelStats)

        class TestModelStats2(ModelStats):
            slug = 'unique_slug'
        self.admin_site.register_stats(TestModel, TestModelStats2)

        # If slugs were identical, there would be only 1 stat here.
        eq_(len(self.admin_site.stats), 2)
