from mock import Mock, patch
from nose.tools import eq_, ok_

from affiliates.base.milestones import MilestoneDisplay
from affiliates.base.tests import aware_date, aware_datetime, TestCase
from affiliates.links.tests import DataPointFactory, LinkFactory
from affiliates.users.tests import UserFactory


class MilestoneDisplayTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.display = MilestoneDisplay(self.user)

        self.display.milestone_date = Mock()
        self.display.milestone_cmp = Mock()
        self.display.surrounding_milestones = Mock()
        self.display.close_to_milestone = Mock()
        self.display.metric_milestones = [5, 10, 20, 50]
        self.display.creation_milestones = [3, 5, 10]

        self.messages = {
            'nothing_yet': 'nothing_yet_{0}',
            'close_to_milestone': 'close_to_milestone_{0}',
            'achieved_milestone': 'achieved_milestone_{0}',
            'total_next_milestone': 'total_next_milestone_{0}_{1}',
            'total_no_milestone': 'total_no_milestone_{0}',
            'link_created': 'link_created'
        }

    def test_iter(self):
        self.display.milestone_cmp.side_effect = lambda a, b: a - b
        self.display.metric_milestone = Mock(side_effect=[1, 2])
        self.display.creation_milestone = Mock(side_effect=[3, 4])

        eq_(list(self.display), [1, 2, 3, 4])

    def test_metric_milestone_no_metric(self):
        """
        If the user has not received any counts for the metric yet,
        return the future date and the nothing_yet message.
        """
        self.user.metric_aggregate_total = Mock(return_value=0)
        self.user.metric_total = Mock(return_value=0)

        milestone = self.display.metric_milestone('metric', self.messages)
        eq_(milestone, (self.display.future_date, 'nothing_yet_5'))

        self.user.metric_aggregate_total.assert_called_with('metric')
        self.user.metric_total.assert_called_with('metric')

    def test_metric_milestone_close(self):
        """
        If the user is within 10% of the next milestone, return
        yesterday's date and the close_to_milestone message.
        """
        # 18 clicks total, close_to_milestone is True
        self.user.metric_aggregate_total = Mock(return_value=4)
        self.user.metric_total = Mock(return_value=18)
        self.display.surrounding_milestones.return_value = (5, 20)
        self.display.close_to_milestone.return_value = True

        with patch('affiliates.base.milestones.date_yesterday') as date_yesterday:
            milestone = self.display.metric_milestone('metric', self.messages)
            eq_(milestone, (date_yesterday.return_value, 'close_to_milestone_2'))

            self.display.surrounding_milestones.assert_called_with(18, [5, 10, 20, 50])

    def test_metric_milestone_have_date_of_last_milestone(self):
        """
        If the aggregate total is less than the previous milestone
        (meaning we know the date of the last milestone), show the date
        the last milestone was achieved with the achieved_milestone
        message.
        """
        # (aggregate == 4) + (prev_milestone == 5) = Last milestone
        # happened within datapoint range and we have a date.
        # milestone_date returns the date when it happened.
        self.user.metric_aggregate_total = Mock(return_value=4)
        self.user.metric_total = Mock(return_value=18)
        self.display.surrounding_milestones.return_value = (5, 20)
        self.display.close_to_milestone.return_value = False
        self.display.milestone_date.return_value = aware_date(2014, 1, 1)

        milestone = self.display.metric_milestone('metric', self.messages)
        eq_(milestone, (aware_date(2014, 1, 1), 'achieved_milestone_5'))

        self.display.milestone_date.assert_called_with('metric', 5, 4)

    def test_metric_milestone_to_next_milestone(self):
        """
        If we don't know when the last milestone happened, but we know
        what the next one is, return yesterday's date with the
        total_next_milestone message.
        """
        # (aggregate == 6) + (last_milestone == 5) = Last milestone
        # datapoint has been aggregated.
        self.user.metric_aggregate_total = Mock(return_value=6)
        self.user.metric_total = Mock(return_value=6)
        self.display.surrounding_milestones.return_value = (5, 10)
        self.display.close_to_milestone.return_value = False

        with patch('affiliates.base.milestones.date_yesterday') as date_yesterday:
            milestone = self.display.metric_milestone('metric', self.messages)
            eq_(milestone, (date_yesterday.return_value, 'total_next_milestone_6_4'))

    def test_metric_milestone_no_previous(self):
        """
        If there is no previous milestone, and we know what the next one
        is, return yesterday's date with the total_next_milestone
        message.
        """
        # (last_milestone == None) = No milestones achieved yet.
        self.user.metric_aggregate_total = Mock(return_value=3)
        self.user.metric_total = Mock(return_value=3)
        self.display.surrounding_milestones.return_value = (None, 5)
        self.display.close_to_milestone.return_value = False

        with patch('affiliates.base.milestones.date_yesterday') as date_yesterday:
            milestone = self.display.metric_milestone('metric', self.messages)
            eq_(milestone, (date_yesterday.return_value, 'total_next_milestone_3_2'))

    def test_metric_milestone_no_milestone(self):
        """
        If the user has hit all the milestones, and we don't know the
        date of the last milestone they hit, return yesterday's date
        with the total_no_milestone message.
        """
        self.user.metric_aggregate_total = Mock(return_value=100)
        self.user.metric_total = Mock(return_value=110)
        self.display.surrounding_milestones.return_value = (50, None)
        self.display.close_to_milestone.return_value = False

        with patch('affiliates.base.milestones.date_yesterday') as date_yesterday:
            milestone = self.display.metric_milestone('metric', self.messages)
            eq_(milestone, (date_yesterday.return_value, 'total_no_milestone_110'))

    def test_creation_milestone_no_links(self):
        """
        If the user hasn't created any links, return a future date with
        the nothing_yet message.
        """
        milestone = self.display.creation_milestone('test', self.messages)

        # creation_milestone doesn't format the nothing_yet message.
        eq_(milestone, (self.display.future_date, 'nothing_yet_{0}'))

    def test_creation_milestone_close_to_next_milestone(self):
        """
        If the user is within 1 link of the next milestone, return
        yesterday's date with the close_to_milestone message.
        """
        LinkFactory.create_batch(2, banner_type='test', user=self.user)
        self.display.surrounding_milestones.return_value = (None, 3)

        with patch('affiliates.base.milestones.date_yesterday') as date_yesterday:
            milestone = self.display.creation_milestone('test', self.messages)
            eq_(milestone, (date_yesterday.return_value, 'close_to_milestone_3'))

            self.display.surrounding_milestones.assert_called_with(
                2, self.display.creation_milestones)

    def test_creation_milestone_far_from_next_milestone(self):
        """
        If the user isn't close to the next milestone, show the date of
        their last milestone.
        """
        links = LinkFactory.create_batch(4, banner_type='test', user=self.user)
        links[0].created = aware_datetime(2014, 1, 1, 5)
        links[1].created = aware_datetime(2014, 1, 1, 8)
        links[2].created = aware_datetime(2014, 1, 2, 5)  # Winner!
        links[3].created = aware_datetime(2014, 1, 3, 5)
        for link in links:
            link.save()

        self.display.surrounding_milestones.return_value = (3, 10)

        milestone = self.display.creation_milestone('test', self.messages)
        eq_(milestone, (aware_date(2014, 1, 2), 'achieved_milestone_3'))

    def test_creation_milestone_no_next_milestone(self):
        """
        If there is no next milestone, show the date of their last
        milestone.
        """
        links = LinkFactory.create_batch(4, banner_type='test', user=self.user)
        links[0].created = aware_datetime(2014, 1, 1, 5)
        links[1].created = aware_datetime(2014, 1, 1, 8)
        links[2].created = aware_datetime(2014, 1, 2, 5)  # Winner!
        links[3].created = aware_datetime(2014, 1, 3, 5)
        for link in links:
            link.save()

        self.display.surrounding_milestones.return_value = (3, None)

        milestone = self.display.creation_milestone('test', self.messages)
        eq_(milestone, (aware_date(2014, 1, 2), 'achieved_milestone_3'))

    def test_creation_milestone_no_previous_links_created(self):
        """
        If there is no previous milestone, but the user has created at
        least one link (which is normally impossible, as the default
        milestones start at 1), show when their last link was created.
        """
        links = LinkFactory.create_batch(2, banner_type='test', user=self.user)
        links[0].created = aware_datetime(2014, 1, 1, 5)
        links[1].created = aware_datetime(2014, 1, 2, 8)
        for link in links:
            link.save()

        self.display.surrounding_milestones.return_value = (None, 5)

        milestone = self.display.creation_milestone('test', self.messages)
        eq_(milestone, (aware_date(2014, 1, 2), 'link_created'))


def _milestone(*args, **kwargs):
    return aware_date(*args, **kwargs), 'milestone'


class MilestoneDisplayUtilTests(TestCase):
    def test_milestone_date(self):
        user = UserFactory.create()
        display = MilestoneDisplay(user)

        DataPointFactory.create(link_clicks=4, date=aware_date(2014, 1, 1), link__user=user)
        DataPointFactory.create(link_clicks=3, date=aware_date(2014, 1, 2), link__user=user)
        DataPointFactory.create(link_clicks=2, date=aware_date(2014, 1, 3), link__user=user)

        eq_(display.milestone_date('link_clicks', 10, 4), aware_date(2014, 1, 2))

    def test_milestone_date_invalid_metric(self):
        """
        If an invalid metric name is given, raise an AttributeError.
        """
        user = UserFactory.create()
        display = MilestoneDisplay(user)

        DataPointFactory.create(link_clicks=4, date=aware_date(2014, 1, 1), link__user=user)

        with self.assertRaises(AttributeError):
            display.milestone_date('invalid', 2, 1)

    def test_milestone_date_not_reached(self):
        """
        If the milestone hasn't been reached by the user, return None.
        """
        user = UserFactory.create()
        display = MilestoneDisplay(user)

        DataPointFactory.create(link_clicks=4, date=aware_date(2014, 1, 1), link__user=user)

        eq_(display.milestone_date('link_clicks', 8, 2), None)

    def test_milestone_cmp_two_dates(self):
        """
        If both values being compared are dates, return the day
        difference between them.
        """
        eq_(MilestoneDisplay.milestone_cmp(_milestone(2014, 1, 3), _milestone(2014, 1, 1)), -2)
        eq_(MilestoneDisplay.milestone_cmp(_milestone(2014, 1, 1), _milestone(2014, 1, 1)), 0)
        eq_(MilestoneDisplay.milestone_cmp(_milestone(2014, 1, 1), _milestone(2014, 1, 3)), 2)

    def test_milestone_cmp_future_dates(self):
        """
        Future dates should be considered less than normal dates and
        equal to other future dates.
        """
        future_milestone = (MilestoneDisplay.future_date, 'future milestone')
        eq_(MilestoneDisplay.milestone_cmp(future_milestone, _milestone(2014, 1, 1)), -1)
        eq_(MilestoneDisplay.milestone_cmp(_milestone(2014, 1, 1), future_milestone), 1)
        eq_(MilestoneDisplay.milestone_cmp(future_milestone, future_milestone), 0)

    def test_surrounding_milestones(self):
        eq_(MilestoneDisplay.surrounding_milestones(5, [1, 3, 4, 6, 7]), (4, 6))

    def test_surrounding_milestones_first_next(self):
        """
        If the amount is smaller than all the milestones, return None
        for the previous milestone.
        """
        eq_(MilestoneDisplay.surrounding_milestones(5, [8, 10, 15]), (None, 8))

    def test_surrounding_milestones_last_prev(self):
        """
        If the amount is greater than all the milestones, return None
        for the next milestone.
        """
        eq_(MilestoneDisplay.surrounding_milestones(25, [8, 10, 15]), (15, None))

    def test_surrounding_milestones_equal(self):
        """
        If the amount is equal to one of the milestones, return that
        amount as the previous milestone.
        """
        eq_(MilestoneDisplay.surrounding_milestones(5, [3, 5, 8, 10, 15]), (5, 8))

    def test_close_to_milestone(self):
        ok_(MilestoneDisplay.close_to_milestone(9, 10))
        ok_(MilestoneDisplay.close_to_milestone(45, 48))
        ok_(not MilestoneDisplay.close_to_milestone(4, 10))

    def test_close_to_milestone_none(self):
        """If the given milestone is None, return False."""
        ok_(not MilestoneDisplay.close_to_milestone(55, None))
