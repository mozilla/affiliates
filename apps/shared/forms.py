from django import forms


class FormBase(forms.Form):
    """Handles common tasks among forms."""
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        # Add placeholders for fields
        for field, placeholder in self.placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
