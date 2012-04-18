from datetime import datetime

from factory import Factory, LazyAttribute, SubFactory

from stats.tests.models import TestModel, TestModelRel


class TestModelRelFactory(Factory):
    FACTORY_FOR = TestModelRel

    value = False


class TestModelFactory(Factory):
    FACTORY_FOR = TestModel

    other = SubFactory(TestModelRelFactory)
    someflag = True
    mychoice = 'test1'
    unimportant = 0
    datetime = LazyAttribute(lambda a: datetime.now())
