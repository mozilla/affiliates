from django.contrib.auth.models import Permission, User

from mock import patch
from nose.tools import ok_

from affiliates.base.tests import TestCase
from affiliates.users.models import add_default_permissions
from affiliates.users.tests import UserFactory


class AddDefaultPermissionsTests(TestCase):
    def setUp(self):
        self.can_share_website = Permission.objects.get(codename='can_share_website')

    def test_not_created(self):
        """If user is not new, don't bother with permissions."""
        user = UserFactory.create()
        user.user_permissions.clear()

        add_default_permissions(User, created=False, instance=user)
        ok_(self.can_share_website not in user.user_permissions.all())

    def test_permission_doesnt_exist(self):
        """
        If the can_share_website permission isn't created yet, do
        nothing.
        """
        user = UserFactory.create()
        user.user_permissions.clear()

        with patch('affiliates.users.models.Permission') as MockPermission:
            MockPermission.DoesNotExist = Exception
            MockPermission.objects.get.side_effect = MockPermission.DoesNotExist

            add_default_permissions(User, created=True, instance=user)
            ok_(self.can_share_website not in user.user_permissions.all())

    def test_permission_granted(self):
        """
        Newly created users should be granted the can_share_website
        permission.
        """
        user = UserFactory.create()
        user.user_permissions.clear()

        add_default_permissions(User, created=True, instance=user)
        ok_(self.can_share_website in user.user_permissions.all())
