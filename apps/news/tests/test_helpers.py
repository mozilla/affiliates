import test_utils
from nose.tools import eq_

from news.models import NewsItem
from news.helpers import get_latest_newsitem


class TestLatestNewsItem(test_utils.TestCase):
    def setUp(self):
        # Create newsitems so we have a reference to them.
        self.news1 = self._news(enabled=True)
        self.news2 = self._news(enabled=False)

    def test_basic(self):
        eq_(get_latest_newsitem(), self.news1)

    def test_none(self):
        self.news1.enabled = False
        self.news1.save()

        eq_(get_latest_newsitem(), None)

    def _news(self, title='Test', content='TestContent', enabled=True):
        news = NewsItem(title=title, content=content, enabled=enabled)
        news.save()

        return news
