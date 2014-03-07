from factory import DjangoModelFactory, Sequence, SubFactory

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


class ImageBannerVariationFactory(DjangoModelFactory):
    FACTORY_FOR = models.ImageBannerVariation

    banner = SubFactory(ImageBannerFactory)
    color = 'Blue'
    locale = 'en-us'
    image = 'uploads/banners/test.png'


class TextBannerFactory(BannerFactory):
    FACTORY_FOR = models.TextBanner


class TextBannerVariationFactory(DjangoModelFactory):
    FACTORY_FOR = models.TextBannerVariation

    banner = SubFactory(TextBannerFactory)
    locale = 'en-us'
    text = Sequence(lambda n: 'test{0}'.format(n))
