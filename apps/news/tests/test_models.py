import test_utils
from nose.tools import eq_

from news.models import NewsItem


class TestCurrent(test_utils.TestCase):
    def setUp(self):
        # Create newsitems so we have a reference to them.
        self.news1 = self._news(enabled=True)
        self.news2 = self._news(enabled=False)

    def test_basic(self):
        eq_(NewsItem.objects.current(), self.news1)

    def test_none(self):
        self.news1.enabled = False
        self.news1.save()

        eq_(NewsItem.objects.current(), None)

    def _news(self, title='Test', content='TestContent', enabled=True):
        news = NewsItem(title=title, content=content, enabled=enabled)
        news.save()

        return news
