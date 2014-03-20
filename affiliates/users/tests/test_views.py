from mock import Mock, patch
from nose.tools import eq_, ok_

from affiliates.base.tests import TestCase
from affiliates.users import views
from affiliates.users.tests import UserFactory


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.view = views.UserProfileView()

    def test_post_user_mismatch(self):
        """
        If the user being edited doesn't match the current user,
        redirect to the profile page for the user being edited without
        making any changes.
        """
        request_user = UserFactory.create()
        request = Mock(user=request_user)

        edited_user = UserFactory.create(display_name='Bob')
        self.view.get_object = Mock(return_value=edited_user.userprofile)

        # Redirect should be called and given the profile, while the
        # parent's post should not be called.
        with patch('affiliates.users.views.UpdateView.post') as super_post:
            with patch('affiliates.users.views.redirect') as redirect:
                eq_(self.view.post(request, edited_user.pk), redirect.return_value)
                redirect.assert_called_with(edited_user.userprofile)
                ok_(not super_post.called)

    def test_post(self):
        user = UserFactory.create()
        request = Mock(user=user)
        self.view.get_object = Mock(return_value=user.userprofile)

        # Defer to the parent's post.
        with patch('affiliates.users.views.UpdateView.post') as super_post:
            eq_(self.view.post(request, user.pk), super_post.return_value)
            super_post.assert_called_with(request, user.pk)
