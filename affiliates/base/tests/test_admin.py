from mock import Mock
from nose.tools import eq_

from affiliates.base.admin import NewsItemModelAdmin
from affiliates.base.models import NewsItem
from affiliates.base.tests import NewsItemFactory, TestCase
from affiliates.users.tests import UserFactory


class NewsItemModelAdminTests(TestCase):
    def setUp(self):
        self.model_admin = NewsItemModelAdmin(NewsItem, Mock())

    def test_save_model_no_pk(self):
        """
        If a NewsItem isn't saved yet (has no pk), set the author to the
        request's current user.
        """
        newsitem = NewsItemFactory.build()
        request = Mock(user=UserFactory.create())

        self.model_admin.save_model(request, newsitem, None, False)
        eq_(newsitem.author, request.user)

    def test_save_model_with_pk(self):
        """
        If a NewsItem exists in the DB (has a pk), do not change the
        author.
        """
        original_author = UserFactory.create()
        newsitem = NewsItemFactory.create(author=original_author)
        request = Mock(user=UserFactory.create())

        self.model_admin.save_model(request, newsitem, None, False)
        eq_(newsitem.author, original_author)
