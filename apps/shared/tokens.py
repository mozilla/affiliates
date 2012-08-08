import time

from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import int_to_base36, base36_to_int


class TokenGenerator(object):
    """
    Strategy object used to generate tokens that can be used for various types
    of temporary verifications, such as account activation or password resets.
    Based heavily off of django.contrib.auth.tokens.
    """

    def __init__(self, state_callable, delay=60 * 60 * 24):
        """
        Seeds the generator with a callable that will return a string.

        An important property of the callable is that, after the action that is
        being verified takes place, the callable should return a different
        string. This ensures that a generated token cannot be reused after the
        action, as the token is based off of the string.

        Typically this should return some concatenation of a model's state, such
        as the password of a user and their last-logged-in time for a password
        reset verification.

        delay specifies the time that a token should be valid in seconds.
        """
        self.state_callable = state_callable
        self.delay = delay

    def generate_token(self):
        return self._generate_token(self.state_callable(), int(time.time()))

    def verify_token(self, token):
        try:
            ts_b36, hash = token.split('-')
        except ValueError:
            return False

        try:
            timestamp = base36_to_int(ts_b36)
        except ValueError:
            return False

        reference_token = self._generate_token(self.state_callable(), timestamp)
        if not constant_time_compare(reference_token, token):
            return False

        if (int(time.time()) - timestamp) > self.delay:
            return False

        return True

    def _generate_token(self, obj_state, timestamp):
        ts_b36 = int_to_base36(timestamp)
        key_salt = 'shared.tokens.generate_token'
        value = unicode(obj_state) + unicode(timestamp)
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return '{0}-{1}'.format(ts_b36, hash)
