from datetime import date, timedelta

from django.core.management.base import CommandError
from django.db import IntegrityError

from mock import patch
from nose.tools import eq_, ok_

from affiliates.base.tests import aware_datetime, TestCase
from affiliates.links.google_analytics import AnalyticsError
from affiliates.links.management.commands import collect_ga_data, update_leaderboard
from affiliates.links.models import LeaderboardStanding
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

        with patch.object(collect_ga_data, 'timezone') as mock_timezone:
            mock_timezone.now.return_value = aware_datetime(2014, 1, 2)
            self.command.execute()

        self.service.get_clicks_for_date.assert_called_with(date(2014, 1, 1))
        ok_(link1.datapoint_set.filter(date=date(2014, 1, 1), link_clicks=4).exists())
        ok_(link2.datapoint_set.filter(date=date(2014, 1, 1), link_clicks=7).exists())


class UpdateLeaderboardTests(TestCase):
    def setUp(self):
        self.command = update_leaderboard.Command()

    def _link_with_clicks(self, user, aggregate_link_clicks, link_click_counts):
        """
        Create a link with a specific number of aggregate links and
        datapoints with the given click counts.
        """
        start_date = date(2014, 4, 1)
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
