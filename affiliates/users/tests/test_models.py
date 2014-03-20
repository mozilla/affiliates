from django.contrib.auth.models import Permission, User

from mock import patch
from nose.tools import eq_, ok_

from affiliates.base.tests import TestCase
from affiliates.users.models import add_default_permissions, UserProfile
from affiliates.users.tests import UserFactory


class UserTests(TestCase):
    def test_display_name_none(self):
        """
        If a user's profile has no display name set, return a localized
        default.
        """
        user = UserFactory.create()
        user.userprofile.display_name = ''

        with patch('affiliates.users.models._') as ugettext:
            ugettext.return_value = 'Affiliate'
            eq_(user.display_name, 'Affiliate')
            ugettext.assert_called_with(u'Affiliate')

    def test_display_name(self):
        user = UserFactory.create()
        user.userprofile.display_name = 'Bob'
        eq_(user.display_name, 'Bob')


class CreateProfileTests(TestCase):
    def test_create_profile(self):
        """Create an empty profile for newly-created users."""
        user = UserFactory.build()

        # Profile doesn't exist yet.
        with self.assertRaises(UserProfile.DoesNotExist):
            user.userprofile

        # After saving, empty profile should exist.
        user.save()
        profile_pk = user.userprofile.pk
        ok_(profile_pk is not None)

        # If we save again, profile should not have been replaced.
        user.userprofile.display_name = 'Bob'
        user.userprofile.save()
        user = User.objects.get(pk=user.pk)
        eq_(user.userprofile.pk, profile_pk)


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
