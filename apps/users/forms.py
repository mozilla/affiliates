import re

from django import forms
from django.forms.util import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from tower import ugettext as _
from tower import ugettext_lazy as _lazy

from users.models import UserProfile


PASSWD_MATCH = _lazy('Passwords must match.')
PASSWD_LENGTH = _lazy('Passwords must be at least 8 characters long.')
PASSWD_COMPLEX = _lazy('Passwords must contain at least 1 letter and '
                       '1 number.')


class PasswordField(forms.CharField):
    """Field for displaying a password input."""

    error_messages = {
        'min_length': PASSWD_LENGTH,
    }

    def __init__(self, *args, **kwargs):
        defaults = {
            'label': _lazy(u'Password'),
            'widget': forms.PasswordInput(render_value=False),
            'min_length': 8,
            'error_messages': PasswordField.error_messages,
        }
        defaults.update(kwargs)
        return super(PasswordField, self).__init__(*args, **defaults)

    def clean(self, value):
        """Passwords must consist of letters and numbers."""
        cleaned_value = super(PasswordField, self).clean(value)

        if cleaned_value:
            # Unicode letters are anything in \w that isn't a digit or _
            letters = re.search(r'(?Lu)[^\W\d_]+', cleaned_value)
            numbers = re.search(r'(?Lu)\d+', cleaned_value)
            if not (letters and numbers):
                raise ValidationError(PASSWD_COMPLEX)

        return cleaned_value


# TODO: Prevent common passwords
class RegisterForm(forms.Form):
    """Form used to create registration profile."""
    name = forms.CharField(label=_lazy(u'Name'), max_length=255)
    email = forms.EmailField(label=_lazy(u'Email'), max_length=255)
    password = PasswordField()


class LoginForm(AuthenticationForm):
    """Form for logging in."""
    remember_me = forms.BooleanField(label=_lazy('Remember me'),
                                     required=False)


class ProfileForm(forms.ModelForm):
    """Parent class for editing UserProfiles."""
    class Meta:
        model = UserProfile

    placeholders = {
        'address_1': _lazy('Street'),
        'address_2': _lazy('Apartment or Unit # (optional)'),
        'city': _lazy('City'),
        'state': _lazy('State or Province'),
    }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Style select fields correctly
        self.fields['locale'].widget.attrs['class'] = 'js_uniform'
        self.fields['country'].widget.attrs['class'] = 'js_uniform'

        # Add placeholders for fields
        for field, placeholder in ProfileForm.placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder


class EditProfileForm(ProfileForm):
    """Form for editing an existing UserProfile."""
    password = PasswordField(label=_lazy(u'New Password'), required=False)
    password2 = PasswordField(label=_lazy(u'Retype Password'), required=False)

    class Meta(ProfileForm.Meta):
        exclude = ('user', 'modified', 'created')

    def save(self, *args, **kwargs):
        """Save password to user object instead of UserProfile."""
        if self.is_valid():
            user = self.instance.user
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])

            user.save()

        return super(EditProfileForm, self).save(*args, **kwargs)

    def clean(self):
        # Passwords must match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password == password2:
            self._errors['password'] = self.error_class([PASSWD_MATCH])
        elif password:
            self.cleaned_data['password'] = password

        return self.cleaned_data


class ActivationForm(ProfileForm):
    """Form used during activation."""
    username = forms.CharField(label=_lazy(u'Username'), max_length=50)

    class Meta(ProfileForm.Meta):
        exclude = ('user', 'modified', 'created', 'name')

    def clean_username(self):
        """Ensure that the chosen username is unique."""
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_('This username is already taken! '
                                          'Please try again.'))
        except User.DoesNotExist:
            pass

        return self.cleaned_data['username']
