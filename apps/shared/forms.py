from django import forms

from product_details import product_details

from shared.models import LocaleField


ENGLISH_LANGUAGE_CHOICES = sorted(
    [(key.lower(), u'{0} ({1})'.format(key, value['English']))
     for key, value in product_details.languages.items()]
    )


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
    def __init__(self, *args, **kwargs):
        super(AdminModelForm, self).__init__(*args, **kwargs)

        # If there are any LocaleFields in this form, we want to display the
        # locale names in English in the admin interface.
        model_fields = self.Meta.model._meta.fields
        for field in model_fields:
            if isinstance(field, LocaleField):
                # Change choices for form field to English choices.
                self.fields[field.name].choices = ENGLISH_LANGUAGE_CHOICES
