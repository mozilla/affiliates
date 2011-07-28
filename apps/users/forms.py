from django import forms

from tower import ugettext_lazy as _lazy

from users.models import UserProfile


# TODO: Confirm constraints on user data
# TODO: Prevent common passwords
class RegisterForm(forms.Form):
    """Form used to create registration profile."""
    name = forms.CharField(label=_lazy(u'Name:'), max_length=255)
    email = forms.EmailField(label=_lazy(u'Email:'), max_length=255)
    password = forms.CharField(label=_lazy(u'Password:'),
                               widget=forms.PasswordInput(render_value=False),
                               min_length=6, max_length=255)


class ProfileForm(forms.ModelForm):
    """Form used to edit user profile."""
    class Meta:
        model = UserProfile
