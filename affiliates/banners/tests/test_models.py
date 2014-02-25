from django.core.exceptions import ValidationError

from nose.tools import eq_, ok_
from mock import Mock, patch

from affiliates.banners.models import Banner
from affiliates.banners.tests import (CategoryFactory, ImageBannerVariationFactory,
                                      TextBannerFactory)
from affiliates.base.tests import TestCase
from affiliates.links.models import Link
from affiliates.users.tests import UserFactory


class CategoryTests(TestCase):
    def test_category_clean(self):
        """
        If a category is more than one layer away from its root, clean
        should raise a ValidationError.
        """
        root = CategoryFactory.create()
        child = CategoryFactory.create(parent=root)
        grandchild = CategoryFactory.create(parent=child)

        root.clean()  # No layers is fine!
        child.clean()  # 1 layer is fine!
        with self.assertRaises(ValidationError):
            grandchild.clean()  # 2 layers is no bueno!


class BannerTests(TestCase):
    def test_create_link(self):
        """
        create_link should create a Link object using this banner's
        description and generated code.
        """
        banner = Banner(destination='https://www.mozilla.org')
        banner.generate_banner_code = Mock(return_value="""
            <a href="{href}">Link!</a>
        """)
        user = UserFactory.create()

        with patch.object(Link, 'get_referral_url') as get_referral_url:
            get_referral_url.return_value = 'asdf'
            link = banner.create_link(user, foo='bar', baz=1)

        ok_(isinstance(link, Link))
        eq_(link.user, user)
        eq_(link.destination, 'https://www.mozilla.org')
        self.assertHTMLEqual(link.html, """
            <a href="asdf">Link!</a>
        """)
        banner.generate_banner_code.assert_called_with(foo='bar', baz=1)


class ImageBannerTests(TestCase):
    def test_generate_banner_code(self):
        # This is less a test of initial correctness and more to alert
        # us of unexpected changes to banner code generation.
        variation = ImageBannerVariationFactory(banner__destination='https://www.mozilla.org',
                                                image='uploads/banners/test.png')
        banner = variation.banner

        with self.settings(MEDIA_URL='/media/'):
            self.assertHTMLEqual(banner.generate_banner_code(variation), """
              <a href="{href}">
                <img src="/media/uploads/banners/test.png">
              </a>
            """)


class ImageBannerVariationTests(TestCase):
    def test_size(self):
        variation = ImageBannerVariationFactory.build()
        variation.image = Mock(width=250, height=140)
        eq_(variation.size, '250x140')


class TextBannerTests(TestCase):
    def test_generate_banner_code(self):
        banner = TextBannerFactory(text='<a href="{href}">Test</a>')
        eq_(banner.generate_banner_code(), '<a href="{href}">Test</a>')
