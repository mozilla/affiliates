from django import forms

from affiliates.users.models import UserProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'website', 'bio')
