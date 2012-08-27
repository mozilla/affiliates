from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from product_details import product_details
from tower import ugettext as _, ugettext_lazy as _lazy

from facebook.models import FacebookBanner, FacebookBannerInstance, FacebookUser
from shared.forms import AdminModelForm
from shared.models import ENGLISH_LANGUAGE_CHOICES
from shared.utils import absolutify

# L10n: &hellip; is an ellipses, the three dots like "I love Firefox because..."
_text_placeholder = _lazy('I love Firefox because&hellip;')


class EmailInput(forms.TextInput):
    """Input specifically for email addresses."""
    input_type = 'email'

    def __init__(self, *args, **kwargs):
        super(EmailInput, self).__init__(*args, **kwargs)
        if not 'placeholder' in self.attrs.keys():
            self.attrs['placeholder'] = _lazy('Enter e-mail')


class BannerFieldRenderer(forms.widgets.RadioFieldRenderer):
    """Custom field renderer for the BannerInstance creation form."""
    def render(self):
        """Render the image grid for the banner selector."""
        banner_ids = [int(banner_id) for banner_id, label in self.choices
                      if banner_id != '']
        banners = dict((banner.id, banner) for banner in
                       FacebookBanner.objects.filter(id__in=banner_ids))

        inputs = []
        for radio_input in self:
            # Ignore empty choice.
            # TODO: Could probably use a better workaround.
            if radio_input.choice_value == '':
                continue

            banner = banners[int(radio_input.choice_value)]

            # Construct image tag.
            img = '<img%s>' % flatatt({
                'class': 'banner-choice',
                'src': absolutify(banner.image.url),
                'width': 100,
                'height': 72,
                'alt': banner.alt_text
            })

            # Add attributes to the input tag.
            radio_input.attrs['data-image'] = absolutify(banner.image.url)

            if 'id' in self.attrs:
                label_for = ' for="%s_%s"' % (radio_input.attrs['id'],
                                              radio_input.index)
            else:
                label_for = ''

            # Bring it all together!
            inputs.append('<label%(label_for)s>\n%(input)s\n%(img)s\n'
                          '</label>' % {
                'label_for': label_for,
                'input': radio_input.tag(),
                'img': img
            })

        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % tag for tag in inputs]))


class BannerRadioSelect(forms.RadioSelect):
    renderer = BannerFieldRenderer


class FacebookBannerInstanceForm(forms.ModelForm):
    use_profile_image = forms.BooleanField(required=False)
    text = forms.CharField(max_length=90, widget=forms.Textarea(attrs={
        # L10n: &hellip; is an ellipses, the three dots like
        # L10n: "I love Firefox because..."
        'placeholder': mark_safe(_text_placeholder),
        'maxlength': 90,
        'rows': 2,
        'required': 'required'
    }), error_messages={
        'max_length': _lazy('Sorry. Your message is too long. Please tell the '
                            'world why you love Firefox in 90 characters or '
                            'less.')
    })

    def __init__(self, request, *args, **kwargs):
        super(FacebookBannerInstanceForm, self).__init__(*args, **kwargs)

        # Remove cols attribute from text widget.
        del self.fields['text'].widget.attrs['cols']

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
        widgets = {
            'banner': BannerRadioSelect(attrs={'required': 'required'}),
        }


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
    affiliates_email = forms.EmailField(
        widget=EmailInput(attrs={'required': 'required'}))

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


class LeaderboardFilterForm(forms.Form):
    country = forms.ChoiceField(choices=settings.COUNTRIES.items())

    def __init__(self, *args, **kwargs):
        super(LeaderboardFilterForm, self).__init__(*args, **kwargs)

        # Update choices to use the current locale.
        lang = get_language()
        choices = sorted(product_details.get_regions(lang).items(),
                         key=lambda n: n[1])
        # L10n: Used in a dropdown that lets users filter the Leaderboard by
        # L10n: country. Refers to the default filter, which shows all countries
        choices.insert(0, ('', _('All')))

        self.fields['country'].choices = choices

    # TODO: Change this into a queryset method.
    def get_top_users(self, limit=25):
        """
        Return the top users ranked by banner clicks and filtered by country
        based on the country field value on this form.
        """
        queryset = (FacebookUser.objects.exclude(leaderboard_position=-1)
                    .order_by('leaderboard_position'))
        if self.is_valid() and self.cleaned_data['country'] != '':
            queryset = queryset.filter(country=self.cleaned_data['country'])

        return queryset[:limit]


class NewsletterSubscriptionForm(forms.Form):
    # L10n: Used in a choice field where users can choose between receiving
    # L10n: HTML-based or Text-only newsletter emails.
    NEWSLETTER_FORMATS = (('html', 'HTML'), ('text', _lazy('Text')))

    email = forms.CharField(widget=EmailInput(attrs={
        'placeholder': _lazy('Your email address'), 'required': 'required'
    }))
    country = forms.ChoiceField(choices=settings.COUNTRIES.items())
    format = forms.ChoiceField(choices=NEWSLETTER_FORMATS, initial='html',
                               widget=forms.RadioSelect())
    privacy_policy_agree = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'required': 'required'}))

    def __init__(self, user, *args, **kwargs):
        super(NewsletterSubscriptionForm, self).__init__(*args, **kwargs)

        # TODO: Figure out how to not duplciate code from the
        # LeaderboardFilterForm. The main issue right now is that ChoiceFields
        # have nothing that runs when a form using it is initiated.

        # Update choices to use the current locale.
        lang = get_language()
        choices = sorted(product_details.get_regions(lang).items(),
                         key=lambda n: n[1])
        self.fields['country'].choices = choices

        self.fields['country'].initial = user.country
