from django.core.cache.backends.dummy import DummyCache
from django.db.models import Sum

from mock import patch
from nose.tools import eq_

from badges.models import BadgeInstance
from banners.tasks import add_click, old_add_click
from shared.tests import TestCase


def _get_clicks(instance_id):
    return (BadgeInstance.objects.get(pk=instance_id).clickstats_set
            .aggregate(Sum('clicks'))['clicks__sum'])


def _get_normalized_clicks(instance_id):
    return BadgeInstance.objects.get(pk=instance_id).clicks


@patch('caching.base.cache', DummyCache(None, {}))
class AddClickTests(TestCase):
    fixtures = ['banners']

    def test_basic(self):
        """Test that the task increments the correct clickstats object."""
        old_clicks = _get_clicks(2)
        add_click(2)
        new_clicks = _get_clicks(2)

        eq_(old_clicks + 1, new_clicks)

    def test_normalized(self):
        """Test that the task increments the normalized click count as well."""
        old_clicks = _get_normalized_clicks(2)
        add_click(2)
        new_clicks = _get_normalized_clicks(2)

        eq_(old_clicks + 1, new_clicks)


@patch('caching.base.cache', DummyCache(None, {}))
class OldAddClickTests(TestCase):
    fixtures = ['banners']

    def _click(self, user_id, instance_id, image_id):
        old_add_click(user_id, instance_id, image_id)

    def test_basic(self):
        old_clicks = _get_clicks(2)
        self._click(1, 1, 1)
        new_clicks = _get_clicks(2)

        eq_(old_clicks + 1, new_clicks)

    def test_normalized_clicks(self):
        old_clicks = _get_normalized_clicks(2)
        self._click(1, 1, 1)

        new_clicks = _get_normalized_clicks(2)
        eq_(old_clicks + 1, new_clicks)
