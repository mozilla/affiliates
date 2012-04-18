from django.contrib.auth.models import User

from factory import Factory, Sequence


class UserFactory(Factory):
    FACTORY_FOR = User
    username = Sequence(lambda n: 'test%s' % n)
    email = Sequence(lambda n: 'test%s@example.com' % n)
