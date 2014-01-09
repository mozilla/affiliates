from django.db import models

from nose.tools import eq_

from affiliates.shared.forms import AdminModelForm
from affiliates.shared.models import LocaleField
from affiliates.shared.tests import TestCase


class AdminModelFormTests(TestCase):
    def test_localefield_choices(self):
        """
        Test that any LocaleFields in the form use English labels for the
        field choices.
        """
        class TestLocaleFieldModel(models.Model):
            locale = LocaleField()

        class TestForm(AdminModelForm):
            class Meta:
                model = TestLocaleFieldModel

        f = TestForm()
        labels = dict(f.fields['locale'].choices)

        # Since product_details rarely changes, assuming what names it will
        # provide for each locale is safe enough for this test.
        eq_(labels['it'], 'it (Italian)')
        eq_(labels['ko'], 'ko (Korean)')
