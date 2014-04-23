import json

from django.http import Http404
from django.test.client import RequestFactory

from mock import Mock, patch
from nose.tools import eq_

from affiliates.banners import views
from affiliates.banners.tests import (CategoryFactory, ImageBannerFactory, TextBannerFactory,
                                      TextBannerVariationFactory)
from affiliates.base.tests import patch_super, TestCase


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
        with patch_super(self.view, 'dispatch') as super_dispatch:
            response = self.view.dispatch(self.factory.get('/'), category_pk=category.pk)
            eq_(response, super_dispatch.return_value)

        eq_(self.view.category, category)

    def test_get_queryset(self):
        """
        The list returned by get_queryset should contain both image
        banners and text banners.
        """
        category = CategoryFactory.create()
        image_banner1, image_banner2 = ImageBannerFactory.create_batch(2, category=category)
        text_banner1, text_banner2 = TextBannerFactory.create_batch(2, category=category)
        self.view.category = category

        eq_(set(self.view.get_queryset()),
            set([image_banner1, image_banner2, text_banner1, text_banner2]))



class CustomizeBannerViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.MockBanner = Mock()

        class TestCustomizeBannerView(views.CustomizeBannerView):
            banner_class = self.MockBanner

            def get_form_kwargs(self):
                return {'foo': 'bar', 'baz': 1}

        self.view = TestCustomizeBannerView()

    def test_get_form(self):
        """
        get_form should pass self.banner as the first argument to the
        form class.
        """
        form_class = Mock()
        self.view.banner = Mock()

        form = self.view.get_form(form_class)
        eq_(form, form_class.return_value)
        form_class.assert_called_with(self.view.banner, foo='bar', baz=1)

    def test_form_valid(self):
        """
        If the form is valid, create a link from the view's banner and
        redirect to the link's detail page.
        """
        self.view.request = Mock()
        self.view.banner = Mock()
        link = self.view.banner.create_link.return_value
        link.get_absolute_url.return_value = '/foo/bar'
        form = Mock(cleaned_data={'foo': 'bar', 'baz': 1})

        with patch('affiliates.banners.views.redirect') as redirect:
            response = self.view.form_valid(form)
            eq_(response, redirect.return_value)
            redirect.assert_called_with('/foo/bar?generator=1')

        self.view.banner.create_link.assert_called_with(self.view.request.user, foo='bar', baz=1)


class CustomizeImageBannerViewTests(TestCase):
    def test_get_context_data_variations(self):
        view = views.CustomizeImageBannerView()
        view.banner = Mock()

        variation1 = Mock(pk=1, locale='en-us', color='Blue', size='100x200',
                          **{'image.url': 'foo.png'})
        variation2 = Mock(pk=2, locale='de', color='Red', size='150x250',
                          **{'image.url': 'bar.png'})
        view.banner.variation_set.all.return_value = [variation1, variation2]

        ctx = view.get_context_data(foo='bar', baz=1)
        eq_(ctx['foo'], 'bar')
        eq_(ctx['baz'], 1)

        variations = json.loads(ctx['variations_json'])
        eq_(variations['1'],
            {'locale': 'en-us', 'color': 'Blue', 'image': 'foo.png', 'size': '100x200'})
        eq_(variations['2'],
            {'locale': 'de', 'color': 'Red', 'image': 'bar.png', 'size': '150x250'})


class CustomizeTextBannerViewTests(TestCase):
    def test_get_context_data_variations(self):
        view = views.CustomizeTextBannerView()
        view.banner = TextBannerFactory.create()

        variation1, variation2 = TextBannerVariationFactory.create_batch(2, banner=view.banner)

        ctx = view.get_context_data(foo='bar', baz=1)
        eq_(ctx['foo'], 'bar')
        eq_(ctx['baz'], 1)

        variations = json.loads(ctx['variations_text_json'])
        eq_(variations, {
            unicode(variation1.pk): variation1.text,
            unicode(variation2.pk): variation2.text,
        })
