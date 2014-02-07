from django import forms

from affiliates.banners.models import ImageBannerVariation


class CustomizeImageBannerForm(forms.Form):
    variation = forms.ModelChoiceField(ImageBannerVariation.objects.none(),
                                       widget=forms.HiddenInput)

    def __init__(self, image_banner, *args, **kwargs):
        super(CustomizeImageBannerForm, self).__init__(*args, **kwargs)

        # Variation field choices are limited by image banner.
        self.fields['variation'].queryset = image_banner.variation_set.all()
