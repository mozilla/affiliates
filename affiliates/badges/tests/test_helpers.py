from datetime import datetime

from jinja2 import Markup
from nose.tools import eq_
from test_utils import TestCase
from tower import activate

from affiliates.badges.helpers import babel_date, babel_number, clean, linkify


class TestHelpers(TestCase):

    def test_clean_basic(self):
        html = 'Text <span>with</span> html.'
        expect = 'Text &lt;span&gt;with&lt;/span&gt; html.'
        eq_(clean(html), Markup(expect))

    def test_clean_whitelist(self):
        html = 'Text <span>with</span> whitelisted <div>html</div>.'
        expect = ('Text <span>with</span> whitelisted &lt;div&gt;html'
                  '&lt;/div&gt;.')
        eq_(clean(html, tags=['span']), Markup(expect))

    def test_linkify(self):
        text = 'Test http://www.mozilla.org text'
        expect = ('Test <a href="http://www.mozilla.org" rel="nofollow">'
                  'http://www.mozilla.org</a> text')
        eq_(linkify(text), Markup(expect))

    def test_linkify_email(self):
        text = 'Test affiliates@mozilla.org text'
        expect = ('Test <a href="mailto:affiliates@mozilla.org" '
                  'rel="nofollow">affiliates@mozilla.org</a> text')
        eq_(linkify(text, parse_email=True), Markup(expect))

    def test_babel_date(self):
        date = datetime(2011, 9, 23)
        activate('en-US')
        eq_(babel_date(date, 'short'), '9/23/11')
        eq_(babel_date(date, 'medium'), 'Sep 23, 2011')

        activate('fr')
        eq_(babel_date(date, 'short'), '23/09/11')
        eq_(babel_date(date, 'medium'), '23 sept. 2011')

    def test_babel_number(self):
        number = 1000000
        activate('en-US')
        eq_(babel_number(number), u'1,000,000')

        activate('fr')
        # \xa0 is a non-breaking space
        eq_(babel_number(number), u'1\xa0000\xa0000')
