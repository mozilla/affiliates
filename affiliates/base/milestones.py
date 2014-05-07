from django.contrib.contenttypes.models import ContentType

from tower import ugettext_lazy as _lazy

from affiliates.banners.models import ImageBanner, TextBanner
from affiliates.base.utils import date_yesterday
from affiliates.links.models import DataPoint


class MilestoneDisplay(object):
    """
    Calculates and stores recently-achieved milestones for display on
    the dashboard and user profile.

    Milestones consist of a date and a string describing the milestone
    achieved. They're calculated on demand rather than stored to avoid
    having to store unnecessary milestones for inactive users.
    """
    metric_milestones = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    creation_milestones = [1, 3, 5, 7, 10, 20]

    link_click_messages = {
        'close_to_milestone': _lazy('Almost {0} clicks!'),
        'achieved_milestone': _lazy('Drove {0} clicks!'),
        'total_next_milestone': _lazy('Drove {0} clicks. That\'s {1} clicks away from the next '
                                      'milestone!'),
        'total_no_milestone': _lazy('Driven {0} clicks in total!'),
        'nothing_yet': _lazy('Drive {0} clicks!'),
    }
    firefox_download_messages = {
        'close_to_milestone': _lazy('Almost {0} downloads!'),
        'achieved_milestone': _lazy('Drove {0} downloads!'),
        'total_next_milestone': _lazy('Drove {0} downloads. That\'s {1} downloads away from the '
                                      'next milestone!'),
        'total_no_milestone': _lazy('Driven {0} downloads in total!'),
        'nothing_yet': _lazy('Drive {0} downloads!'),
    }
    image_banner_messages = {
        'nothing_yet': _lazy('Create a banner!'),
        'close_to_milestone': _lazy('Almost {0} banners created!'),
        'achieved_milestone': _lazy('Created {0} banners!'),
        'link_created': _lazy('Created a banner.'),
    }
    text_banner_messages = {
        'nothing_yet': _lazy('Create a text link!'),
        'close_to_milestone': _lazy('Almost {0} text links created!'),
        'achieved_milestone': _lazy('Created {0} text links!'),
        'link_created': _lazy('Created a text link.'),
    }

    future_date = None

    def __init__(self, user):
        self.user = user
        self.milestones = None

    def __iter__(self):
        if not self.milestones:
            self.milestones = sorted([
                self.metric_milestone('link_clicks', self.link_click_messages),
                self.metric_milestone('firefox_downloads', self.firefox_download_messages),
                self.creation_milestone(ImageBanner, self.image_banner_messages),
                self.creation_milestone(TextBanner, self.text_banner_messages),
            ], self.milestone_cmp)
        return iter(self.milestones)

    def metric_milestone(self, metric, messages):
        """
        :param metric:
            Name of the metric to use, e.g. link_clicks.
        :param messages:
            Dictionary of messages to choose from.
        :return:
            Tuple of (milestone date, message).
        """
        metric_aggregate_total = self.user.metric_aggregate_total(metric)
        metric_total = self.user.metric_total(metric)

        # If the user has nothing at all, show a "future" milestone.
        if metric_total == 0:
            return (self.future_date,
                    unicode(messages['nothing_yet']).format(self.metric_milestones[0]))

        # Find the last milestone we passed and the next one.
        prev_milestone, next_milestone = self.surrounding_milestones(metric_total,
                                                                     self.metric_milestones)

        # If we are within 10% of the next milestone, show a message.
        if self.close_to_milestone(metric_total, next_milestone):
            remaining = next_milestone - metric_total
            return (date_yesterday(), unicode(messages['close_to_milestone']).format(remaining))

        # If the last milestone happened within the Datapoint
        # retentation period, show when it happened.
        if prev_milestone and metric_aggregate_total < prev_milestone:
            milestone_date = self.milestone_date(metric, prev_milestone, metric_aggregate_total)
            if milestone_date:
                return (milestone_date,
                        unicode(messages['achieved_milestone']).format(prev_milestone))

        # As a last resort, show the metric total as of yesterday.
        if next_milestone:
            difference = next_milestone - metric_total
            return (date_yesterday(),
                    unicode(messages['total_next_milestone']).format(metric_total, difference))
        else:
            return date_yesterday(), unicode(messages['total_no_milestone']).format(metric_total)

    def creation_milestone(self, banner_class, messages):
        """
        :param banner_class:
            Class for the type of banner used to create links used for
            this milestone, e.g. TextBanner.
        :param messages:
            Dictionary of messages to choose from.
        """
        links = filter(lambda link: isinstance(link.banner, banner_class),
                       self.user.link_set.all())
        link_count = len(links)

        # If no links have been created, show a future milestone.
        if link_count == 0:
            return self.future_date, unicode(messages['nothing_yet'])

        prev_milestone, next_milestone = self.surrounding_milestones(link_count,
                                                                     self.creation_milestones)

        # If we are within 1 link of the next milestone, show a message.
        if next_milestone and next_milestone - link_count == 1:
            return date_yesterday(), unicode(messages['close_to_milestone']).format(next_milestone)

        # As a last resort, show their previous milestone.
        sorted_links = sorted(links, lambda x, y: cmp(x.created, y.created))
        if prev_milestone:
            milestone_link = sorted_links[prev_milestone - 1]
            return (milestone_link.created.date(),
                    unicode(messages['achieved_milestone']).format(prev_milestone))

        # This shouldn't ever happen (no previous milestone yet at least
        # one banner created), but just in case, show when the last link
        # was created.
        return sorted_links[-1].created.date(), unicode(messages['link_created'])

    def milestone_date(self, metric, milestone, aggregated_amount):
        """
        Find the date that the user achieved the given milestone.

        :param metric:
            Name of the metric to check against, e.g. link_clicks.
        :param milestone:
            Milestone that we want to find the date of.
        :param aggregated_amount:
            Aggregated total for the metric we're checking. Must be less
            than the milestone.
        :return:
            The date the milestone was achieved, or None if it could not
            be found.
        """
        datapoints = DataPoint.objects.filter(link__user=self.user).order_by('date')
        amount = aggregated_amount

        for datapoint in datapoints:
            amount += getattr(datapoint, metric)
            if amount > milestone:
                return datapoint.date

        return None

    @classmethod
    def milestone_cmp(cls, milestone1, milestone2):
        """
        Compare milestones by date, putting future dates in front of
        normal ones.
        """
        date1 = milestone1[0]
        date2 = milestone2[0]

        if date1 == cls.future_date:
            return 0 if date2 == cls.future_date else -1
        elif date2 == cls.future_date:
            return 0 if date1 == cls.future_date else 1
        else:
            return (date2 - date1).days

    @staticmethod
    def surrounding_milestones(amount, milestones):
        """
        Return the two milestone amounts that the given amount is
        between. If the amount is equal to a milestone, the returned
        milestones will be the current amount and the next milestone.

        :param amount:
            Current amount to find surrounding milestones for.
        :param milestones:
            List of milestones to check against.
        :return:
            Tuple of (last milestone, next milestone).
        """
        prev_milestone = None
        next_milestone = None
        for i, milestone in enumerate(milestones):
            if milestone > amount:
                next_milestone = milestone
                break
            else:
                prev_milestone = milestone

            # End of the list? No more milestones!
            if i == len(milestones) - 1:
                next_milestone = None

        return prev_milestone, next_milestone

    @staticmethod
    def close_to_milestone(amount, milestone):
        """
        Determine if the given amount is within 10% of the milestone.
        """
        return milestone and amount + (milestone / 10) >= milestone
