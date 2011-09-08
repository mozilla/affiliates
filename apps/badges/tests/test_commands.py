from django.core import management

from nose.tools import eq_
from test_utils import TestCase

from badges.models import Leaderboard


class TestUpdateLeaderboard(TestCase):
    fixtures = ['leaderboard']

    def test_basic(self):
        management.call_command('update_leaderboard')

        actual = Leaderboard.objects.order_by('ranking').values_list()
        expected = [
            (1, 11, 2005028),
            (2, 15, 1),
            (3, 16, 1),
            (4, 12, 0),
            (5, 13, 0),
            (6, 14, 0),
        ]
        for i, val in enumerate(expected):
            eq_(actual[i], val)
