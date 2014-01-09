from django.contrib.auth.models import User

from nose.tools import ok_
from test_utils import TestCase

from affiliates.users.helpers import gravatar_url


class TestGravatars(TestCase):
    fixtures = ['registered_users']

    def test_basic(self):
        url = gravatar_url('mkelly@mozilla.com')
        ok_('a414aea4a5b11c6e2e00f760e96b85ab' in url)

    def test_user(self):
        user = User.objects.get(email='mkelly@mozilla.com')
        url = gravatar_url(user)
        ok_('a414aea4a5b11c6e2e00f760e96b85ab' in url)
