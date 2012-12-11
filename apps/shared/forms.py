from django import forms

from tower import ugettext_lazy as _lazy


class FormBase(forms.Form):
    """Handles common tasks among forms."""
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        # Add placeholders for fields
        for field_name, placeholder in self.placeholders.items():
            field = self.fields[field_name]
            field.widget.attrs['placeholder'] = placeholder


class AdminModelForm(forms.ModelForm):
    """Special form class that handles admin-interface-specific changes."""
    pass  # Retained for possible future use.


class EmailInput(forms.TextInput):
    """Input specifically for email addresses."""
    input_type = 'email'

    def __init__(self, *args, **kwargs):
        super(EmailInput, self).__init__(*args, **kwargs)
        if not 'placeholder' in self.attrs.keys():
            self.attrs['placeholder'] = _lazy('Enter e-mail')


class NewsletterForm(forms.Form):
    email = forms.CharField(widget=EmailInput(attrs={
        'placeholder': _lazy('Your email address'), 'required': 'required'
    }))
