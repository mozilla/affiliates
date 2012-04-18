from django.test.client import RequestFactory

from nose.tools import eq_, ok_

from shared.tests import ModelsTestCase
from stats.filters import FilterSpec
from stats.tests import TestModelFactory, TestModelRelFactory
from stats.tests.models import TestModel, TestModelRel


def _request(url='/test', **kwargs):
    return RequestFactory().get(url, data=kwargs)


def test_filter_type():
    """Test that the filter type is correctly detected."""
    tests = [
        ('relation', 'other'),
        ('boolean', 'someflag'),
        ('choice', 'mychoice'),
        (None, 'unimportant'),
        ('boolean', 'other__value')
    ]
    for filter_type, filter_name in tests:
        filter_spec = FilterSpec(_request(), TestModel, filter_name)
        yield eq_, filter_type, filter_spec.type


def test_filter_value():
    """Test that the filter value is correctly parsed."""
    tests = [
        (4L, '4', 'other'),
        (False, '', 'someflag'),
        ('test1', 'test1', 'mychoice'),
        (True, '1', 'other__value')
    ]
    for filter_value, url_argument, filter_name in tests:
        kwargs = {filter_name: url_argument}
        filter_spec = FilterSpec(_request(**kwargs), TestModel, filter_name)
        yield eq_, filter_value, filter_spec.value


class FilterSpecTests(ModelsTestCase):
    apps = ['stats.tests']

    def test_choices_relation(self):
        """Test that the choices for a relation filter include every related
        item.
        """
        TestModelRel.objects.all().delete()
        a = TestModelRelFactory(value=False)
        b = TestModelRelFactory(value=True)

        filter_spec = FilterSpec(_request('/test'), TestModel, 'other')
        choice_urls = [c.link for c in filter_spec.get_choices()]
        eq_(len(choice_urls), 3)
        ok_('/test?' in choice_urls)
        ok_(('/test?other=%s' % a.id) in choice_urls)
        ok_(('/test?other=%s' % b.id) in choice_urls)

    def test_choices_boolean(self):
        """Test that the choices for a boolean filter include True and
        False.
        """
        filter_spec = FilterSpec(_request('/test'), TestModel, 'someflag')
        choice_urls = [c.link for c in filter_spec.get_choices()]
        ok_('/test?' in choice_urls)
        ok_('/test?someflag=True' in choice_urls)
        ok_('/test?someflag=False' in choice_urls)

    def test_choices_choice(self):
        """Test that choices for a choice filter include all available
        choices.
        """
        filter_spec = FilterSpec(_request('/test'), TestModel, 'mychoice')
        choice_urls = [c.link for c in filter_spec.get_choices()]
        eq_(len(choice_urls), 3)
        ok_('/test?' in choice_urls)
        ok_('/test?mychoice=test1' in choice_urls)
        ok_('/test?mychoice=test2' in choice_urls)

    def test_apply_filter(self):
        """Test that apply_filter correctly filters a queryset."""
        ft = TestModelFactory(unimportant=5)
        filter_spec = FilterSpec(_request('/test?unimportant=5'), TestModel,
                                 'unimportant')
        qs = TestModel.objects.all()

        new_qs = filter_spec.apply_filter(qs)
        ok_(ft in new_qs)

    def test_apply_filter_no_value(self):
        """Test that apply_filter will not filter the queryset if there is no
        value in the URL.
        """
        TestModelFactory(unimportant=6)
        filter_spec = FilterSpec(_request('/test'), TestModel, 'unimportant')
        qs = TestModel.objects.all()

        new_qs = filter_spec.apply_filter(qs)
        eq_(list(qs), list(new_qs))
