from nose.tools import ok_

from affiliates.banners.forms import CustomizeImageBannerForm, CustomizeTextBannerForm
from affiliates.banners.tests import (ImageBannerFactory, ImageBannerVariationFactory,
                                      TextBannerFactory, TextBannerVariationFactory)
from affiliates.base.tests import TestCase


class CustomizeImageBannerFormTests(TestCase):
    def test_variation_queryset(self):
        """
        The variation field queryset should be limited to variations
        from the image banner passed in the constructor.
        """
        banner = ImageBannerFactory.create()

        variation1, variation2 = ImageBannerVariationFactory.create_batch(2, banner=banner)
        ok_(CustomizeImageBannerForm(banner, {'variation': variation1.pk}).is_valid())
        ok_(CustomizeImageBannerForm(banner, {'variation': variation2.pk}).is_valid())

        non_matching_variation = ImageBannerVariationFactory.create()
        invalid_form = CustomizeImageBannerForm(banner, {'variation': non_matching_variation.pk})
        ok_(not invalid_form.is_valid())


class CustomizeTextBannerFormTests(TestCase):
    def test_variation_queryset(self):
        """
        The variation field queryset should be limited to variations
        from the text banner passed in the constructor.
        """
        banner = TextBannerFactory.create()

        variation1, variation2 = TextBannerVariationFactory.create_batch(2, banner=banner)
        ok_(CustomizeTextBannerForm(banner, {'variation': variation1.pk}).is_valid())
        ok_(CustomizeTextBannerForm(banner, {'variation': variation2.pk}).is_valid())

        non_matching_variation = TextBannerVariationFactory.create()
        invalid_form = CustomizeTextBannerForm(banner, {'variation': non_matching_variation.pk})
        ok_(not invalid_form.is_valid())
