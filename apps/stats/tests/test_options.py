from datetime import datetime

from django.contrib.admin.sites import AdminSite
from django.db import models
from django.test.client import RequestFactory

from nose.tools import eq_

from shared.tests import ModelsTestCase
from stats.monkeypatches import patch as patch_admin
from stats.options import ModelStats
from stats.tests import TestModelFactory
from stats.tests.models import TestModel


class ModelStatsTests(ModelsTestCase):
    apps = ['stats.tests']

    def _setup_test_models(self, data):
        TestModel.objects.all().delete()
        for unimportant, dt_data in data:
            TestModelFactory(unimportant=unimportant,
                             datetime=datetime(*dt_data))

    def setUp(self):
        self.admin_site = AdminSite()
        patch_admin(self.admin_site)
        self.factory = RequestFactory()

    def test_datetime_field_autodetect(self):
        """Test that the datetime field autodetection works."""
        m = ModelStats(TestModel, self.admin_site)
        eq_(m.datetime_field, 'datetime')

    def test_data_for_period(self):
        """Test that data_for_period returns an accurate time series."""
        class MyModelStats(ModelStats):
            aggregate = models.Sum('unimportant')

        testdata = [
            (5, (2012, 4, 1)),
            (3, (2012, 4, 15)),
            (7, (2012, 5, 10)),
            (8, (2012, 6, 25))
        ]
        self._setup_test_models(testdata)

        m = MyModelStats(TestModel, self.admin_site)
        data = m.data_for_period(TestModel.objects.all(), datetime(2012, 4, 1),
                                 datetime(2012, 6, 30), interval='months')
        expected = [(datetime(2012, 4, 1), 8), (datetime(2012, 5, 1), 7),
                    (datetime(2012, 6, 1), 8)]
        eq_(expected, data)

    def test_aggregate_for_period(self):
        """Test that aggregate_for_period returns an accurate aggregate."""
        class MyModelStats(ModelStats):
            aggregate = models.Sum('unimportant')

        testdata = [
            (5, (2012, 4, 1)),
            (3, (2012, 4, 15)),
            (7, (2012, 5, 10)),
            (8, (2012, 6, 25))
        ]
        self._setup_test_models(testdata)

        m = MyModelStats(TestModel, self.admin_site)
        result = m.aggregate_for_period(TestModel.objects.all(),
                                        datetime(2012, 4, 1),
                                        datetime(2012, 6, 30))
        eq_(result, 23)

    def test_overview_defaults(self):
        """Test that the default parameters are used by the overview view."""
        class MyModelStats(ModelStats):
            aggregate = models.Sum('unimportant')
            default_interval = 'months'
            default_start = lambda self: datetime(2012, 5, 1)
            default_end = lambda self: datetime(2012, 6, 1)

        testdata = [
            (5, (2012, 5, 1)),
            (3, (2012, 6, 1))
        ]
        self._setup_test_models(testdata)

        m = MyModelStats(TestModel, self.admin_site)
        response = m.overview(self.factory.get('/test'))
        expected = [(datetime(2012, 5, 1), 5), (datetime(2012, 6, 1), 3)]
        eq_(expected, response.context_data['results'])

    def test_overview_arguments(self):
        """Test that the overview view will accept GET arguments."""
        class MyModelStats(ModelStats):
            aggregate = models.Sum('unimportant')

        testdata = [
            (5, (2012, 5, 1)),
            (3, (2012, 6, 1))
        ]
        self._setup_test_models(testdata)

        m = MyModelStats(TestModel, self.admin_site)
        args = {'start': datetime(2012, 5, 1), 'end': datetime(2012, 6, 1),
                'interval': 'months'}
        response = m.overview(self.factory.get('/test', args))

        expected = [(datetime(2012, 5, 1), 5), (datetime(2012, 6, 1), 3)]
        eq_(expected, response.context_data['results'])

    def test_overview_filters(self):
        """Test that the overview view applies filters to the data."""
        class MyModelStats(ModelStats):
            aggregate = models.Sum('unimportant')
            filters = ['mychoice']

        TestModel.objects.all().delete()
        TestModelFactory(unimportant=5, datetime=datetime(2012, 5, 1),
                         mychoice='test1')
        TestModelFactory(unimportant=6, datetime=datetime(2012, 5, 1),
                         mychoice='test2')

        m = MyModelStats(TestModel, self.admin_site)
        args = {'start': datetime(2012, 5, 1), 'end': datetime(2012, 5, 10),
                'interval': 'months', 'mychoice': 'test2'}
        response = m.overview(self.factory.get('/test', args))

        eq_(6, response.context_data['aggregate'])
