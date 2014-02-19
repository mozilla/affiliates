from django.test.client import RequestFactory

from nose.tools import ok_

from affiliates.base.tests import TestCase
from affiliates.links.views import LinkDetailView
from affiliates.links.tests import LinkFactory
from affiliates.users.tests import UserFactory


class LinkDetailViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_queryset(self):
        """
        Available links should be limited to those owned by the current
        user.
        """
        request = self.factory.get('/')
        request.user = UserFactory.create()

        link1, link2 = LinkFactory.create_batch(2, user=request.user)
        unowned_link = LinkFactory.create()

        view = LinkDetailView()
        view.request = request
        qs = view.get_queryset()

        ok_(link1 in qs)
        ok_(link2 in qs)
        ok_(unowned_link not in qs)
