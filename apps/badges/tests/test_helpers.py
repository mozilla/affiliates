from jinja2 import Markup
from nose.tools import eq_
from test_utils import TestCase

from badges.helpers import bleach


class TestHelpers(TestCase):

    def test_bleach_basic(self):
        html = 'Text <span>with</span> html.'
        expect = 'Text &lt;span&gt;with&lt;/span&gt; html.'
        eq_(bleach(html), Markup(expect))

    def test_bleach_whitelist(self):
        html = 'Text <span>with</span> whitelisted <div>html</div>.'
        expect = ('Text <span>with</span> whitelisted &lt;div&gt;html'
                  '&lt;/div&gt;.')
        eq_(bleach(html, tags=['span']), Markup(expect))
