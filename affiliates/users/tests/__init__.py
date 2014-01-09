from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

from factory import Factory, Sequence, SubFactory


class UserFactory(Factory):
    FACTORY_FOR = User
    username = Sequence(lambda n: 'test%s' % n)
    email = Sequence(lambda n: 'test%s@example.com' % n)


class ContentTypeFactory(Factory):
    FACTORY_FOR = ContentType
    name = Sequence(lambda n: 'test%s' % n)
    app_label = Sequence(lambda n: 'test%s' % n)
    model = Sequence(lambda n: 'test%s' % n)


class PermissionFactory(Factory):
    FACTORY_FOR = Permission
    name = Sequence(lambda n: 'test%s' % n)
    codename = Sequence(lambda n: 'test%s' % n)
    content_type = SubFactory(ContentTypeFactory)
