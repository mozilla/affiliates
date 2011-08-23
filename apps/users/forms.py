from django import forms
from django.contrib.auth.models import User

from tower import ugettext as _
from tower import ugettext_lazy as _lazy

from users.models import UserProfile
from users.utils import hash_password


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


class ActivationForm(forms.ModelForm):
    """Form used during activation."""
    username = forms.CharField(label=_lazy(u'Username'), max_length=50)
    password = PasswordField(label=_lazy(u'New Password'), required=False)
    password2 = PasswordField(label=_lazy(u'Retype Password'), required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', 'modified', 'created', 'name')

    def clean(self):
        # Passwords must match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password == password2:
            raise forms.ValidationError(_('Passwords must match.'))
        elif password:
            self.cleaned_data['password'] = hash_password(password)

        return self.cleaned_data

    def clean_username(self):
        """Ensure that the chosen username is unique."""
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_('Username is already taken!'))
        except User.DoesNotExist:
            pass

        return self.cleaned_data['username']


class ProfileForm(forms.ModelForm):
    """Form used to edit user profile."""
    class Meta:
        model = UserProfile
