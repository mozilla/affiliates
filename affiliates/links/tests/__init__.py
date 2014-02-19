from datetime import date

from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyDate

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
    date = FuzzyDate(date(2014, 1, 1))
