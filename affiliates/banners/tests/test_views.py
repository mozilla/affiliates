from django.http import Http404
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_

from affiliates.banners import views
from affiliates.banners.tests import CategoryFactory
from affiliates.base.tests import TestCase


class BannerListViewTests(TestCase):
    def setUp(self):
        self.view = views.BannerListView()
        self.factory = RequestFactory()

    def test_dispatch_category_404(self):
        """If no category exists with a matching pk, raise Http404."""
        with self.assertRaises(Http404):
            self.view.dispatch(self.factory.get('/'), category_pk='99999')

    def test_dispatch_category_exists(self):
        """
        If a category with the given pk exists, set that category to
        self.category on the view.
        """
        category = CategoryFactory.create()
        with patch.object(self.view.__class__.__bases__[0], 'dispatch') as super_dispatch:
            response = self.view.dispatch(self.factory.get('/'), category_pk=category.pk)
            eq_(response, super_dispatch.return_value)

        eq_(self.view.category, category)
