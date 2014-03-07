from django import forms

from affiliates.banners.models import ImageBannerVariation, TextBannerVariation


class CustomizeImageBannerForm(forms.Form):
    variation = forms.ModelChoiceField(ImageBannerVariation.objects.none(),
                                       widget=forms.HiddenInput)

    def __init__(self, image_banner, *args, **kwargs):
        super(CustomizeImageBannerForm, self).__init__(*args, **kwargs)

        # Variation field choices are limited by image banner.
        self.fields['variation'].queryset = image_banner.variation_set.all()


class CustomizeTextBannerForm(forms.Form):
    variation = forms.ModelChoiceField(TextBannerVariation.objects.none())

    def __init__(self, text_banner, *args, **kwargs):
        super(CustomizeTextBannerForm, self).__init__(*args, **kwargs)

        # Variation field choices are limited by banner.
        self.fields['variation'].queryset = text_banner.variation_set.all()
