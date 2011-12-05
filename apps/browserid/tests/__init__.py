from django.utils.functional import wraps

from mock import patch


class mock_browserid(object):
    """
    Mocks django_browserid verification. Can be used as a context manager or
    as a decorator:

    with mock_browserid('a@b.com'):
        django_browserid.verify('random-token')  # = {'status': 'okay',
                                                 #    'email': 'a@b.com'}

    @mock_browserid(None)
    def browserid_test():
        django_browserid.verify('random-token')  # = False
    """
    def __init__(self, email=None):
        self.patcher = patch('django_browserid.base._verify_http_request')
        if email is not None:
            self.return_value = {'status': 'okay', 'email': email}
        else:
            self.return_value = {'status': 'failure'}

    def __enter__(self):
        self.patcher.start().return_value = self.return_value

    def __exit__(self, exc_type, exc_value, traceback):
        self.patcher.stop()

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner
