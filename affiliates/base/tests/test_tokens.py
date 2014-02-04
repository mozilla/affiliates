from mock import patch
from nose.tools import eq_

from affiliates.base.tests import TestCase
from affiliates.base.tokens import TokenGenerator


class TokenGeneratorTests(TestCase):
    def generate_token(self, generator, time):
        with patch('affiliates.base.tokens.time.time') as time_func:
            time_func.return_value = time
            return generator.generate_token()

    def verify_token(self, generator, token, time):
        with patch('affiliates.base.tokens.time.time') as time_func:
            time_func.return_value = time
            return generator.verify_token(token)

    def test_token_expires(self):
        """Test that a token expires after the proper delay."""
        gen = TokenGenerator(lambda: 'asdf', delay=10)
        token = self.generate_token(gen, time=10)
        eq_(self.verify_token(gen, token, time=30), False)

    def test_state_change_invalidates_token(self):
        """
        If the state callback returns a different value during validation, the
        token should not be valid.
        """
        value = 'asdf'
        gen = TokenGenerator(lambda: value, delay=100)
        token = self.generate_token(gen, time=10)
        value = '1234'
        eq_(self.verify_token(gen, token, time=30), False)

    def test_valid_token(self):
        """
        If the state callback returns the same value during validation, and
        the time difference is less than the specified delay, the token
        should verify successfully.
        """
        gen = TokenGenerator(lambda: 'asdf', delay=100)
        token = self.generate_token(gen, time=10)
        eq_(self.verify_token(gen, token, time=30), True)
