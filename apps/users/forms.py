from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from tower import ugettext as _
from tower import ugettext_lazy as _lazy

from users.models import UserProfile


class PasswordField(forms.CharField):
    """Field for displaying a password input."""
    def __init__(self, label=_lazy(u'Password'),
                 widget=forms.PasswordInput(render_value=False),
                 min_length=6, max_length=255, *args, **kwargs):
        return super(PasswordField, self).__init__(label=label, widget=widget,
                                                   min_length=min_length,
                                                   max_length=max_length,
                                                   *args, **kwargs)


# TODO: Confirm constraints on user data
# TODO: Prevent common passwords
class RegisterForm(forms.Form):
    """Form used to create registration profile."""
    name = forms.CharField(label=_lazy(u'Name'), max_length=255)
    email = forms.EmailField(label=_lazy(u'Email'), max_length=255)
    password = PasswordField()


class LoginForm(AuthenticationForm):
    """Form for logging in."""
    remember_me = forms.BooleanField(label=_lazy('Remember me'), required=False)


class ProfileForm(forms.ModelForm):
    """Parent class for editing UserProfiles."""
    class Meta:
        model = UserProfile

    placeholders = {
        'address_1': _('Street'),
        'address_2': _('Apartment or Unit # (optional)'),
        'city': _('City'),
        'state': _('State or Province'),
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
    email = forms.EmailField(label=_lazy(u'Email'))
    password = PasswordField(label=_lazy(u'New Password'), required=False)
    password2 = PasswordField(label=_lazy(u'Retype Password'), required=False)

    class Meta(ProfileForm.Meta):
        exclude = ('user', 'modified', 'created')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Pull email from user object if possible
        if self.instance:
            self.initial['email'] = self.instance.user.email

    def save(self, *args, **kwargs):
        """Save email and password to user object instead of UserProfile."""
        if self.is_valid():
            user = self.instance.user
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])

            user.save()

        return super(EditProfileForm, self).save(*args, **kwargs)

    def clean(self):
        # Passwords must match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password == password2:
            raise forms.ValidationError(_('Passwords must match.'))
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
