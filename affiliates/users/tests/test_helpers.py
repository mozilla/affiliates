from nose.tools import eq_

from affiliates.base.tests import TestCase
from affiliates.users.helpers import gravatar
from affiliates.users.tests import UserFactory


class TestGravatar(TestCase):
    def test_basic(self):
        """Passing an email returns the gravatar url for that email."""
        url = gravatar('test@example.com')
        eq_(url, 'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=80&d=mm')

    def test_user(self):
        """Passing a user returns the gravatar url for that user's email."""
        user = UserFactory.create(email='test@example.com')
        url = gravatar(user)
        eq_(url, 'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=80&d=mm')

    def test_size(self):
        url = gravatar('test@example.com', size=40)
        eq_(url, 'https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=40&d=mm')
