from datetime import datetime

from factory import Factory, LazyAttribute, lazy_attribute, SubFactory

from badges.models import (Category, ClickStats, Badge, BadgeInstance,
                           Subcategory)
from users.tests import UserFactory


class CategoryFactory(Factory):
    FACTORY_FOR = Category

    name = 'TestCategory'


class SubcategoryFactory(Factory):
    FACTORY_FOR = Subcategory

    parent = SubFactory(CategoryFactory)
    name = 'TestSubcategory'


class BadgeFactory(Factory):
    FACTORY_FOR = Badge

    name = 'TestBadge'
    subcategory = SubFactory(SubcategoryFactory)
    href = 'http://www.example.com'
    displayed = True


class BadgeInstanceFactory(Factory):
    FACTORY_FOR = BadgeInstance

    user = SubFactory(UserFactory)
    badge = SubFactory(BadgeFactory)
    clicks = 0


class ClickStatsFactory(Factory):
    FACTORY_FOR = ClickStats

    badge_instance = LazyAttribute(lambda a: BadgeInstanceFactory(clicks=a.clicks))
    clicks = 0

    @lazy_attribute
    def datetime(a):
        now = datetime.now()
        return datetime(now.year, now.month, 1)
