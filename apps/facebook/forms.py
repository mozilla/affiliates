from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from tower import ugettext_lazy as _lazy

from facebook.models import FacebookBanner, FacebookBannerInstance
from shared.forms import AdminModelForm
from shared.models import ENGLISH_LANGUAGE_CHOICES
from shared.utils import absolutify


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
                'height': 72
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
            'banner': BannerRadioSelect(),
            'text': forms.Textarea(attrs={
                # L10n: &hellip; is an ellipses, the three dots like
                # L10n: "I love Firefox because..."
                'placeholder': mark_safe(_text_placeholder),
                'maxlength': 90,
                'rows': 2
            })
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
    affiliates_email = forms.EmailField(widget=EmailInput())

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
