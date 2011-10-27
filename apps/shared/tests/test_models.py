from mock import patch
from nose.tools import eq_, ok_

from shared.tests import models, ModelsTestCase


class ModelBaseTests(ModelsTestCase):
    apps = ['shared.tests']

    @patch('shared.models._')
    def localized_basic_test(self, _):
        # Category inherits from ModelBase
        c = models.ModelBaseChild.objects.create(name='TestString')
        c.localized('name')
        _.assert_called_with('TestString')

    def localized_cache_test(self):
        c = models.ModelBaseChild.objects.create(name='TestString')
        ok_('name' not in c._localized_attrs)

        c.localized('name')
        ok_('name' in c._localized_attrs)


class MultiTableParentModelTests(ModelsTestCase):
    apps = ['shared.tests']

    def setUp(self):
        self.child = models.MultiTableChild.objects.create(some_value=10)

    def test_child(self):
        parent = models.MultiTableParent.objects.all()[0]
        eq_(parent.child_type, 'multitablechild')
        eq_(parent.child(), self.child)
