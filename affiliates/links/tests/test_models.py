from datetime import date

from nose.tools import eq_

from affiliates.base.tests import TestCase
from affiliates.links.models import Link
from affiliates.links.tests import DataPointFactory, LinkFactory


class LinkTests(TestCase):
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
