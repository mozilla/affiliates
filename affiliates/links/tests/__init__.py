from factory import DjangoModelFactory, Sequence, SubFactory

from affiliates.links import models
from affiliates.users.tests import UserFactory


class LinkFactory(DjangoModelFactory):
    FACTORY_FOR = models.Link

    user = SubFactory(UserFactory)
    destination = 'https://www.mozilla.org'
    html = '<a href="{href}">Test!</a>'


class DataPointFactory(DjangoModelFactory):
    FACTORY_FOR = models.DataPoint

    link = SubFactory(LinkFactory)


class LeaderboardStandingFactory(DjangoModelFactory):
    FACTORY_FOR = models.LeaderboardStanding

    ranking = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    metric = 'link_clicks'
