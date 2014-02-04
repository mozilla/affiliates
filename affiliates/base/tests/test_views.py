from funfactory.urlresolvers import reverse
from nose.tools import eq_

from affiliates.base.tests import TestCase


class ErrorPageTests(TestCase):
    def _get(self, url):
        with self.activate('en-US'):
            return self.client.get(reverse(url))

    def test_404(self):
        response = self._get('404')
        eq_(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_facebook_404(self):
        response = self._get('facebook.404')
        eq_(response.status_code, 404)
        self.assertTemplateUsed(response, 'facebook/error.html')

    def test_500(self):
        response = self._get('500')
        eq_(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')

    def test_facebook_500(self):
        response = self._get('facebook.500')
        eq_(response.status_code, 500)
        self.assertTemplateUsed(response, 'facebook/error.html')
