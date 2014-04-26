from nose.tools import eq_
from mock import patch

from affiliates.base.tests import TestCase
from affiliates.links import helpers
from affiliates.links.tests import LeaderboardStandingFactory


class LeaderboardTests(TestCase):
    def test_basic(self):
        l1 = LeaderboardStandingFactory(metric='link_clicks', ranking=1)
        l2 = LeaderboardStandingFactory(metric='link_clicks', ranking=2)
        l3 = LeaderboardStandingFactory(metric='link_clicks', ranking=3)
        l4 = LeaderboardStandingFactory(metric='link_clicks', ranking=4)
        l5 = LeaderboardStandingFactory(metric='link_clicks', ranking=5)
        LeaderboardStandingFactory(metric='link_clicks', ranking=6)
        LeaderboardStandingFactory(metric='firefox_downloads', ranking=1)

        with patch('affiliates.links.helpers.render_to_string') as render_to_string:
            helpers.leaderboard(metric='link_clicks', count=5)
            ctx = render_to_string.call_args[0][1]
            eq_(list(ctx['standings']), [l1, l2, l3, l4, l5])
