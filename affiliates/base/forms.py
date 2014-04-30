from django import forms
from django.conf import settings

from tower import ugettext_lazy as _lazy


COUNTRY_CHOICES = sorted(settings.COUNTRIES.items(),  lambda a, b: cmp(a[1], b[1]))


class EmailInput(forms.TextInput):
    """Input specifically for email addresses."""
    input_type = 'email'


class NewsletterSubscriptionForm(forms.Form):
    # L10n: Used in a choice field where users can choose between receiving
    # L10n: HTML-based or Text-only newsletter emails.
    NEWSLETTER_FORMATS = (('html', 'HTML'), ('text', _lazy('Text')))

    email = forms.CharField(
        widget=EmailInput(attrs={'required': 'required', 'aria-required': 'true'}))
    country = forms.ChoiceField(choices=[('', _lazy('-- select --'))] + COUNTRY_CHOICES)
    format = forms.ChoiceField(choices=NEWSLETTER_FORMATS)
    privacy_policy_agree = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'required': 'required', 'aria-required': 'true'}))
