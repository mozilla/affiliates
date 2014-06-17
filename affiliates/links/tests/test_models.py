from datetime import date

from nose.tools import eq_

from affiliates.base.tests import aware_date, TestCase
from affiliates.links.models import Link
from affiliates.links.tests import DataPointFactory, LinkFactory


class LinkTests(TestCase):
    def test_get_metric_total(self):
        """
        _get_metric_total should combine the aggregate data on the link
        and the data stored in multiple data points.
        """
        link = LinkFactory.create(aggregate_link_clicks=58)
        DataPointFactory.create(link=link, link_clicks=5, date=aware_date(2014, 1, 1))
        DataPointFactory.create(link=link, link_clicks=2, date=aware_date(2014, 1, 2))
        DataPointFactory.create(link=link, link_clicks=87, date=aware_date(2014, 1, 3))

        eq_(link._get_metric_total('link_clicks'), 58 + 5 + 2 + 87)

    def test_manager_total_link_clicks(self):
        for clicks in (4, 6, 9, 10):  # = 29 clicks
            DataPointFactory.create(link_clicks=clicks, date=date(2014, 4, 26))
        for clicks in (25, 5, 5):  # = 35 clicks
            LinkFactory.create(aggregate_link_clicks=clicks)

        # Create a link with multiple datapoints to test for a faulty
        # join that would screw up the totals.
        link = LinkFactory.create()
        DataPointFactory.create(link_clicks=7, link=link, date=date(2014, 4, 26))
        DataPointFactory.create(link_clicks=7, link=link, date=date(2014, 4, 27))


        # 29 + 35 + 7 + 7 = 78 clicks
        eq_(Link.objects.total_link_clicks(), 78)
