from datetime import date, datetime

from django.core.management.base import CommandError
from django.db import IntegrityError

from mock import patch
from nose.tools import ok_

from affiliates.base.tests import TestCase
from affiliates.links.google_analytics import AnalyticsError
from affiliates.links.management.commands import collect_ga_data
from affiliates.links.tests import LinkFactory


class CollectGADataTests(TestCase):
    def setUp(self):
        self.command = collect_ga_data.Command()

        # Mock AnalyticsService to prevent API requests during tests.
        patcher = patch.object(collect_ga_data, 'AnalyticsService')
        self.addCleanup(patcher.stop)

        self.AnalyticsService = patcher.start()
        self.service = self.AnalyticsService.return_value

    def test_error_creating_service(self):
        """
        If there's an error creating the service, raise a CommandError.
        """
        self.AnalyticsService.side_effect = AnalyticsError
        with self.assertRaises(CommandError):
            self.command.handle()

    def test_error_downloading_click_counts(self):
        """
        If there's an error downloading click counts, raise a
        CommandError.
        """
        self.service.get_clicks_for_date.side_effect = AnalyticsError
        with self.assertRaises(CommandError):
            self.command.handle()

    def test_integrity_error_bulk_create(self):
        """
        If an IntegrityError is raised during bulk_create, raise a
        CommandError.
        """
        link1, link2 = LinkFactory.create_batch(2)
        self.service.get_clicks_for_date.return_value = {
            unicode(link1.pk): '4',
            unicode(link2.pk): '7'
        }

        with patch.object(collect_ga_data, 'DataPoint') as MockDataPoint:
            MockDataPoint.objects.bulk_create.side_effect = IntegrityError

            with self.assertRaises(CommandError):
                self.command.execute()

    def test_success(self):
        link1, link2 = LinkFactory.create_batch(2)
        self.service.get_clicks_for_date.return_value = {
            unicode(link1.pk): '4',
            unicode(link2.pk): '7'
        }

        with patch.object(collect_ga_data, 'datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2014, 1, 2)
            self.command.execute()

        self.service.get_clicks_for_date.assert_called_with(date(2014, 1, 1))
        ok_(link1.datapoint_set.filter(date=date(2014, 1, 1), link_clicks=4).exists())
        ok_(link2.datapoint_set.filter(date=date(2014, 1, 1), link_clicks=7).exists())
