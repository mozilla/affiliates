from factory import DjangoModelFactory, Sequence, SubFactory

from affiliates.banners.tests import TextBannerVariationFactory
from affiliates.links import models
from affiliates.users.tests import UserFactory


class LinkFactory(DjangoModelFactory):
    FACTORY_FOR = models.Link

    user = SubFactory(UserFactory)
    html = '<a href="{href}">Test!</a>'
    banner_variation = SubFactory(TextBannerVariationFactory)


class DataPointFactory(DjangoModelFactory):
    FACTORY_FOR = models.DataPoint

    link = SubFactory(LinkFactory)


class LeaderboardStandingFactory(DjangoModelFactory):
    FACTORY_FOR = models.LeaderboardStanding

    ranking = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    metric = 'link_clicks'
