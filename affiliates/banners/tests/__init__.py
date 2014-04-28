from django.db.models.signals import post_init

from factory import DjangoModelFactory, Sequence, SubFactory
from factory.django import mute_signals

from affiliates.banners import models


class CategoryFactory(DjangoModelFactory):
    FACTORY_FOR = models.Category

    name = Sequence(lambda n: 'test{0}'.format(n))


class BannerFactory(DjangoModelFactory):
    ABSTRACT_FACTORY = True

    category = SubFactory(CategoryFactory)
    name = Sequence(lambda n: 'test{0}'.format(n))
    destination = 'https://mozilla.org/'
    visible = True


class ImageBannerFactory(BannerFactory):
    FACTORY_FOR = models.ImageBanner


@mute_signals(post_init)
class ImageVariationFactory(DjangoModelFactory):
    ABSTRACT_FACTORY = True

    color = 'Blue'
    locale = 'en-us'
    image = 'uploads/image_banners/test.png'


class ImageBannerVariationFactory(ImageVariationFactory):
    FACTORY_FOR = models.ImageBannerVariation

    banner = SubFactory(ImageBannerFactory)


class TextBannerFactory(BannerFactory):
    FACTORY_FOR = models.TextBanner


class TextBannerVariationFactory(DjangoModelFactory):
    FACTORY_FOR = models.TextBannerVariation

    banner = SubFactory(TextBannerFactory)
    locale = 'en-us'
    text = Sequence(lambda n: 'test{0}'.format(n))


class FirefoxUpgradeBannerFactory(BannerFactory):
    FACTORY_FOR = models.FirefoxUpgradeBanner


@mute_signals(post_init)
class FirefoxUpgradeBannerVariationFactory(ImageVariationFactory):
    FACTORY_FOR = models.FirefoxUpgradeBannerVariation

    banner = SubFactory(FirefoxUpgradeBannerFactory)
    image = 'uploads/firefox_upgrade_banners/test.png'
    upgrade_image = 'uploads/firefox_upgrade_banners/test_upgrade.png'
