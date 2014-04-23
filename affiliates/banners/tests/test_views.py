import json

from django.http import Http404
from django.test.client import RequestFactory

from mock import Mock, patch
from nose.tools import eq_

from affiliates.banners import views
from affiliates.banners.models import TextBanner
from affiliates.banners.tests import (CategoryFactory, FirefoxUpgradeBannerFactory,
                                      ImageBannerFactory, TextBannerFactory,
                                      TextBannerVariationFactory)
from affiliates.base.tests import patch_super, TestCase


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.view = views.CategoryListView()

    def test_get_queryset_visible_banners(self):
        """
        get_queryset should return a queryset with only categories that
        have visible banners.
        """
        parent = CategoryFactory.create()
        category1, category2, category3, category4 = CategoryFactory.create_batch(4, parent=parent)

        # category1 has a visible ImageBanner
        ImageBannerFactory.create(category=category1, visible=True)
        TextBannerFactory.create(category=category1, visible=False)
        FirefoxUpgradeBannerFactory.create(category=category1, visible=False)

        # category2 has a visible TextBanner
        ImageBannerFactory.create(category=category2, visible=False)
        TextBannerFactory.create(category=category2, visible=True)
        FirefoxUpgradeBannerFactory.create(category=category2, visible=False)

        # category3 has a visible FirefoxUpgradeBanner
        ImageBannerFactory.create(category=category3, visible=False)
        TextBannerFactory.create(category=category3, visible=False)
        FirefoxUpgradeBannerFactory.create(category=category3, visible=True)

        # category4 has no visible banners
        ImageBannerFactory.create(category=category4, visible=False)
        TextBannerFactory.create(category=category4, visible=False)
        FirefoxUpgradeBannerFactory.create(category=category4, visible=False)

        eq_(set(self.view.get_queryset()), set([category1, category2, category3]))


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
        The list returned by get_queryset should contain image banners,
        text banners, and upgrade banners.
        """
        category = CategoryFactory.create()
        image_banner1, image_banner2 = ImageBannerFactory.create_batch(
            2, category=category, visible=True)
        text_banner1, text_banner2 = TextBannerFactory.create_batch(
            2, category=category, visible=True)
        upgrade_banner1, upgrade_banner2 = FirefoxUpgradeBannerFactory.create_batch(
            2, category=category, visible=True)
        self.view.category = category

        # Create banners with visible=False that should not show up.
        ImageBannerFactory.create(category=category, visible=False)
        TextBannerFactory.create(category=category, visible=False)
        FirefoxUpgradeBannerFactory.create(category=category, visible=False)

        eq_(set(self.view.get_queryset()),
            set([image_banner1, image_banner2, text_banner1, text_banner2, upgrade_banner1,
                 upgrade_banner2]))



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
        form = Mock(cleaned_data={'variation': 'bar'})

        with patch('affiliates.banners.views.redirect') as redirect:
            response = self.view.form_valid(form)
            eq_(response, redirect.return_value)
            redirect.assert_called_with('/foo/bar?generator=1')

        self.view.banner.create_link.assert_called_with(self.view.request.user, 'bar')

    def test_dispatch_invalid_pk(self):
        """If an invalid PK is given to dispatch, raise an Http404."""
        self.view.banner_class = TextBanner
        with self.assertRaises(Http404):
            self.view.dispatch(pk=999999999)

    def test_dispatch_invisible(self):
        self.view.banner_class = TextBanner
        banner = TextBannerFactory.create(visible=False)

        with self.assertRaises(Http404):
            self.view.dispatch(pk=banner.pk)


class CustomizeImageBannerViewTests(TestCase):
    def test_get_context_data_variations(self):
        view = views.CustomizeImageBannerView()
        view.banner = Mock()

        variation1 = Mock(pk=1, locale='en-us', color='Blue', size='100x200',
                          **{'image.url': 'foo.png'})
        variation2 = Mock(pk=2, locale='de', color='Red', size='150x250',
                          **{'image.url': 'bar.png'})
        view.banner.variation_set.all.return_value = [variation1, variation2]

        with patch('affiliates.banners.views.locale_to_native') as locale_to_native:
            locale_to_native.side_effect = lambda k: {'en-us': 'English', 'de': 'German'}[k]
            ctx = view.get_context_data(foo='bar', baz=1)
        eq_(ctx['foo'], 'bar')
        eq_(ctx['baz'], 1)

        variations = json.loads(ctx['variations_json'])
        eq_(variations['1'],
            {'locale': 'English', 'color': 'Blue', 'image': 'foo.png', 'size': '100x200'})
        eq_(variations['2'],
            {'locale': 'German', 'color': 'Red', 'image': 'bar.png', 'size': '150x250'})


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
