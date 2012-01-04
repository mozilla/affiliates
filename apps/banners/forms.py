from django import forms

from banners.models import BannerImage
from shared.forms import FormBase


class BannerForm(FormBase):
    image = forms.ModelChoiceField(BannerImage.objects.all(),
                                   widget=forms.HiddenInput())
