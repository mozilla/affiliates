from django.test.utils import override_settings

from nose.tools import eq_

from affiliates.base.tests import TestCase
from affiliates.users.helpers import gravatar
from affiliates.users.tests import UserFactory


@override_settings(SITE_URL='https://example.com')
class TestGravatar(TestCase):
    default = 'https%3A%2F%2Fexample.com%2Fstatic%2Fimg%2Favatar.png'

    def test_basic(self):
        """Passing an email returns the gravatar url for that email."""
        url = gravatar('test@example.com')
        eq_(url,
            'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=80&d={default}'
            .format(default=self.default))

    def test_user(self):
        """Passing a user returns the gravatar url for that user's email."""
        user = UserFactory.create(email='test@example.com')
        url = gravatar(user)
        eq_(url,
            'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=80&d={default}'
            .format(default=self.default))

    def test_size(self):
        url = gravatar('test@example.com', size=40)
        eq_(url,
            'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=40&d={default}'
            .format(default=self.default))
