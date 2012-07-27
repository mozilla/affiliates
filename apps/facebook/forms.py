from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from facebook.models import FacebookBanner, FacebookBannerInstance
from shared.forms import AdminModelForm
from shared.models import ENGLISH_LANGUAGE_CHOICES


class FacebookBannerInstanceForm(forms.ModelForm):
    class Meta:
        model = FacebookBannerInstance
        fields = ('banner', 'text', 'can_be_an_ad')


class FacebookBannerAdminForm(AdminModelForm):
    locales = forms.MultipleChoiceField(
        required=False,
        choices=ENGLISH_LANGUAGE_CHOICES,
        widget=FilteredSelectMultiple('locales', is_stacked=False))

    class Meta:
        model = FacebookBanner

    def __init__(self, *args, **kwargs):
        """Populate locale field from instance."""
        super(FacebookBannerAdminForm, self).__init__(*args, **kwargs)

        locales = self.instance.locale_set.all()
        self.fields['locales'].initial = [l.locale for l in locales]
