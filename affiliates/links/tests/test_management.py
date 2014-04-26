from datetime import timedelta

from django.core.management.base import CommandError

from mock import patch
from nose.tools import eq_, ok_

from affiliates.base.tests import aware_date, aware_datetime, TestCase
from affiliates.links.google_analytics import AnalyticsError
from affiliates.links.management.commands import (aggregate_old_datapoints, collect_ga_data,
                                                  update_leaderboard)
from affiliates.links.models import DataPoint, LeaderboardStanding, Link
from affiliates.links.tests import DataPointFactory, LeaderboardStandingFactory, LinkFactory
from affiliates.users.tests import UserFactory


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

    def test_default_yesterday(self):
        """When no date is given, fetch data for the previous day."""
        link1, link2 = LinkFactory.create_batch(2)
        self.service.get_clicks_for_date.return_value = {
            unicode(link1.pk): '4',
            unicode(link2.pk): '7'
        }
        yesterday = aware_datetime(2014, 1, 1).date()

        with patch.object(collect_ga_data, 'date_yesterday') as date_yesterday:
            date_yesterday.return_value = yesterday
            self.command.execute()

        self.service.get_clicks_for_date.assert_called_with(yesterday)
        eq_(link1.datapoint_set.get(date=yesterday).link_clicks, 4)
        eq_(link2.datapoint_set.get(date=yesterday).link_clicks, 7)

    def test_date_argument(self):
        """
        If a date argument is given, parse it as DD-MM-YYYY and use it
        as the query date.
        """
        link1, link2 = LinkFactory.create_batch(2)
        self.service.get_clicks_for_date.return_value = {
            unicode(link1.pk): '4',
            unicode(link2.pk): '7'
        }
        query_date = aware_datetime(2014, 1, 1).date()

        # Create pre-existing data to check that it is replaced.
        DataPointFactory.create(link=link1, date=query_date, link_clicks=18)
        DataPointFactory.create(link=link2, date=query_date, link_clicks=14)

        self.command.execute('01-01-2014')

        # There must only be one datapoint for the query date, and the
        # link_clicks must match the new data.
        self.service.get_clicks_for_date.assert_called_with(query_date)
        eq_(link1.datapoint_set.get(date=query_date).link_clicks, 4)
        eq_(link2.datapoint_set.get(date=query_date).link_clicks, 7)

    def test_invalid_date_argument(self):
        """If the date argument is invalid, raise a CommandError."""
        with self.assertRaises(CommandError):
            self.command.execute('asdgasdihg')


class UpdateLeaderboardTests(TestCase):
    def setUp(self):
        self.command = update_leaderboard.Command()

    def _link_with_clicks(self, user, aggregate_link_clicks, link_click_counts):
        """
        Create a link with a specific number of aggregate links and
        datapoints with the given click counts.
        """
        start_date = aware_date(2014, 4, 1)
        link = LinkFactory.create(user=user, aggregate_link_clicks=aggregate_link_clicks)
        for link_clicks in link_click_counts:
            DataPointFactory.create(link=link, link_clicks=link_clicks, date=start_date)
            start_date += timedelta(1)

    def test_basic(self):
        # Create users and links with the noted number of clicks.

        # User with clicks in both aggregate and datapoints across many
        # links.
        user1 = UserFactory.create() # Total: 38 clicks
        self._link_with_clicks(user1, 5, [4, 6, 3]) # 18 clicks
        self._link_with_clicks(user1, 1, [8, 9, 2]) # 20 clicks

        # User with clicks in both aggregate and datapoints in 1 link.
        user2 = UserFactory.create() # Total: 49 clicks
        self._link_with_clicks(user2, 13, [12, 11, 13]) # 49 clicks

        # User with no links.
        user3 = UserFactory.create() # Total: 0 clicks

        # User with links that have no aggregate clicks or no datapoint
        # clicks.
        user4 = UserFactory.create() # Total: 9 clicks
        self._link_with_clicks(user4, 1, [2, 2]) # 5 clicks
        self._link_with_clicks(user4, 0, [2]) # 2 clicks
        self._link_with_clicks(user4, 2, []) # 2 clicks

        # This one just sort've rounds out the set I guess.
        user5 = UserFactory.create() # Total: 9 clicks
        self._link_with_clicks(user5, 1, [2, 2, 2]) # 7 clicks
        self._link_with_clicks(user5, 0, [2]) # 2 clicks

        self.command.handle()
        eq_([s.user for s in LeaderboardStanding.objects.order_by('ranking')],
            [user2, user1, user4, user5, user3])

    def test_clear_old(self):
        """
        When the leaderboard is updated, old standings should be
        cleared.
        """
        user1 = UserFactory.create() # Total: 38 clicks
        self._link_with_clicks(user1, 5, [4, 6, 3]) # 18 clicks
        self._link_with_clicks(user1, 1, [8, 9, 2]) # 20 clicks

        user2 = UserFactory.create() # Total: 49 clicks
        self._link_with_clicks(user2, 13, [12, 11, 13]) # 49 clicks

        # Create existing leaderboard with users in opposite order.
        LeaderboardStandingFactory.create(user=user1, ranking=1, metric='link_clicks')
        LeaderboardStandingFactory.create(user=user2, ranking=2, metric='link_clicks')

        self.command.handle()
        ok_(not (LeaderboardStanding.objects
                 .filter(user=user1, ranking=1, metric='link_clicks')
                 .exists()))
        ok_(not (LeaderboardStanding.objects
                 .filter(user=user2, ranking=2, metric='link_clicks')
                 .exists()))


class AggregateOldDataPointsTests(TestCase):
    def setUp(self):
        self.command = aggregate_old_datapoints.Command()

    def test_basic(self):
        """
        Aggregate any datapoints older than 90 days into the totals
        stored on their links.
        """
        link1 = LinkFactory.create(aggregate_link_clicks=7, aggregate_firefox_downloads=10)
        link1_old_datapoint = DataPointFactory.create(link=link1, date=aware_date(2014, 1, 1),
                                                      link_clicks=8, firefox_downloads=4)
        link1_new_datapoint = DataPointFactory.create(link=link1, date=aware_date(2014, 3, 1),
                                                      link_clicks=2, firefox_downloads=7)

        link2 = LinkFactory.create(aggregate_link_clicks=7, aggregate_firefox_downloads=10)
        link2_old_datapoint1 = DataPointFactory.create(link=link2, date=aware_date(2014, 1, 1),
                                                       link_clicks=8, firefox_downloads=4)
        link2_old_datapoint2 = DataPointFactory.create(link=link2, date=aware_date(2013, 12, 30),
                                                       link_clicks=2, firefox_downloads=7)

        self.command.handle()

        # link1 should have 7+8=15 clicks, 10+4=14 downloads, and the
        # new datapoint should still exist.
        link1 = Link.objects.get(pk=link1.pk)
        eq_(link1.aggregate_link_clicks, 15)
        eq_(link1.aggregate_firefox_downloads, 14)
        ok_(not DataPoint.objects.filter(pk=link1_old_datapoint.pk).exists())
        ok_(DataPoint.objects.filter(pk=link1_new_datapoint.pk).exists())

        # link2 should have 7+8+2=17 clicks, 10+4+7=21 downloads, and the
        # old datapoints should not exist.
        link2 = Link.objects.get(pk=link2.pk)
        eq_(link2.aggregate_link_clicks, 17)
        eq_(link2.aggregate_firefox_downloads, 21)
        ok_(not DataPoint.objects.filter(pk=link2_old_datapoint1.pk).exists())
        ok_(not DataPoint.objects.filter(pk=link2_old_datapoint2.pk).exists())
