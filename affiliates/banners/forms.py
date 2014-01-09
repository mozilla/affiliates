from django import forms

from affiliates.banners.models import BannerImage
from affiliates.shared.forms import FormBase


class BannerForm(FormBase):
    image = forms.ModelChoiceField(BannerImage.objects.all(),
                                   widget=forms.HiddenInput())
