from django import forms


class FormBase(forms.Form):
    """Handles common tasks among forms."""
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        # Add placeholders for fields
        for field_name, placeholder in self.placeholders.items():
            field = self.fields[field_name]
            field.widget.attrs['placeholder'] = placeholder
