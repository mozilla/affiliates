from factory import DjangoModelFactory, Sequence, SubFactory

from affiliates.banners import models


class CategoryFactory(DjangoModelFactory):
    FACTORY_FOR = models.Category

    name = Sequence(lambda n: 'test{0}'.format(n))


class ImageBannerFactory(DjangoModelFactory):
    FACTORY_FOR = models.ImageBanner

    category = SubFactory(CategoryFactory)
    name = Sequence(lambda n: 'test{0}'.format(n))
    destination = 'https://mozilla.org/'
    visible = True
