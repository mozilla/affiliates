from datetime import date

from nose.tools import eq_

from affiliates.base.tests import TestCase
from affiliates.links.models import DataPoint
from affiliates.links.tasks import add_click
from affiliates.links.tests import DataPointFactory, LinkFactory


class AddClickTests(TestCase):
    def test_link_does_not_exist(self):
        """If the link does not exist, do nothing (but don't fail!)."""
        eq_(add_click(99999999, date(2014, 4, 1)), None)

    def test_link_exists_no_datapoint(self):
        """If not datapoint for the given date exists, create one."""
        link = LinkFactory.create()
        add_click(link.id, date(2014, 4, 1))
        datapoint = link.datapoint_set.get(date=date(2014, 4, 1))
        eq_(datapoint.link_clicks, 1)

    def test_link_exists_datapoint_exists(self):
        """
        If a datapoint exists for the given date, increment it's
        link_clicks value.
        """
        link = LinkFactory.create()
        datapoint = DataPointFactory.create(link=link, date=date(2014, 1, 1), link_clicks=7)

        add_click(link.id, date(2014, 1, 1))
        datapoint = DataPoint.objects.get(pk=datapoint.pk)
        eq_(datapoint.link_clicks, 8)
