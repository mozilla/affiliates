from django import forms

from tower import ugettext_lazy as _lazy

from shared.forms import FormBase
from users.forms import AGREE_TOS_PP, DISPLAY_NAME_REQUIRED


class RegisterForm(FormBase):
    """Form used for BrowserID registration."""
    display_name = forms.CharField(max_length=255, error_messages={
        'required': DISPLAY_NAME_REQUIRED
    })
    agreement = forms.BooleanField(error_messages={'required': AGREE_TOS_PP})
    email_subscribe = forms.BooleanField(required=False)

    placeholders = {
        'display_name': _lazy(u'Your display name'),
    }
