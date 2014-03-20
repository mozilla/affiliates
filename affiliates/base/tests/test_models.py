import jinja2
from nose.tools import eq_, ok_
from mock import ANY, patch

from affiliates.base.tests import NewsItemFactory, NewsItemTranslationFactory, TestCase


class NewsItemTests(TestCase):
    def setUp(self):
        patcher = patch('affiliates.base.models.bleach')
        self.addCleanup(patcher.stop)
        self.bleach = patcher.start()
        self.bleach.clean.return_value = 'cleaned_html'

        patcher = patch('affiliates.base.models.render_to_string')
        self.addCleanup(patcher.stop)
        self.render_to_string = patcher.start()
        self.render_to_string.return_value = 'rendered_html'

    def test_render(self):
        newsitem = NewsItemFactory.create(title='foo', html='<p>bar</p>')

        result = newsitem.render()
        ok_(isinstance(result, jinja2.Markup))
        eq_(result, 'rendered_html')
        self.bleach.clean.assert_called_with('<p>bar</p>', tags=ANY, attributes=ANY)
        self.render_to_string.assert_called_with('base/newsitem.html', {
            'title': 'foo',
            'html': 'cleaned_html'
        })

    def test_render_with_locale(self):
        """
        If a locale is passed to render, use the title and html from the
        matching translation instead of the base NewsItem.
        """
        newsitem = NewsItemFactory.create(title='foo', html='<p>bar</p>')
        NewsItemTranslationFactory.create(newsitem=newsitem, locale='de', title='baz',
                                          html='<p>biff</p>')

        result = newsitem.render(locale='de')
        ok_(isinstance(result, jinja2.Markup))
        eq_(result, 'rendered_html')
        self.bleach.clean.assert_called_with('<p>biff</p>', tags=ANY, attributes=ANY)
        self.render_to_string.assert_called_with('base/newsitem.html', {
            'title': 'baz',
            'html': 'cleaned_html'
        })

    def test_render_with_invalid_locale(self):
        """
        If an invalid locale is passed to render, use the title and html
        from the base NewsItem.
        """
        newsitem = NewsItemFactory.create(title='foo', html='<p>bar</p>')
        NewsItemTranslationFactory.create(newsitem=newsitem, locale='de', title='baz',
                                          html='<p>biff</p>')

        result = newsitem.render(locale='fr')
        ok_(isinstance(result, jinja2.Markup))
        eq_(result, 'rendered_html')
        self.bleach.clean.assert_called_with('<p>bar</p>', tags=ANY, attributes=ANY)
        self.render_to_string.assert_called_with('base/newsitem.html', {
            'title': 'foo',
            'html': 'cleaned_html'
        })
