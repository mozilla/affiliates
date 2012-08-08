from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User

from facebook.models import FacebookBanner, FacebookBannerInstance
from shared.forms import AdminModelForm
from shared.models import ENGLISH_LANGUAGE_CHOICES


class FacebookBannerInstanceForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(FacebookBannerInstanceForm, self).__init__(*args, **kwargs)

        # Limit the banner field to banners available in the current locale.
        # Allows for a missing request locale to allow testing. On a real server
        # the locale is guarenteed to be set by LocaleURLMiddleware.
        request_locale = getattr(request, 'locale', None)
        if request_locale:
            queryset = (FacebookBanner.objects
                        .filter(locale_set__locale__contains=request_locale))
            self.fields['banner'].queryset = queryset

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
        super(FacebookBannerAdminForm, self).__init__(*args, **kwargs)

        # Populates the list of locales from the banner instance's existing
        # values.
        locales = self.instance.locale_set.all()
        self.fields['locales'].initial = [l.locale for l in locales]


class FacebookAccountLinkForm(forms.Form):
    affiliates_email = forms.EmailField()

    def clean_affiliates_email(self):
        """
        Ensure that the email address corresponds to a valid Affiliates account.
        """
        email = self.cleaned_data['affiliates_email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            # English is okay here since this error is never shown to the user.
            raise forms.ValidationError('Affiliates account not found.')
        return email
