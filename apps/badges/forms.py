from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple

from badges.models import BadgeLocale


class BadgeLocaleAdminForm(forms.ModelForm):
    """
    Custom admin form that uses a MultipleChoiceField for choosing enabled
    locales for a badge.

    Adapted from
    http://www.hindsightlabs.com/blog/2010/02/11/adding-extra-fields-to-a-model-form-in-djangos-admin/
    """
    locales = forms.MultipleChoiceField(choices=settings.LANGUAGES.items(),
                                        widget=FilteredSelectMultiple(
                                            "Locales", is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(BadgeLocaleAdminForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            badge_locales = kwargs['instance'].badgelocale_set.all()
            self.initial['locales'] = [bl.locale for bl in badge_locales]

    def save(self, commit=True):
        model = super(BadgeLocaleAdminForm, self).save(commit=False)

        badge_locales = [BadgeLocale(badge=model, locale=locale)
                         for locale in self.cleaned_data['locales']]

        # save_m2m is called after save to handle ManyToMany relationships.
        # Although BadgeLocales aren't ManyToMany, they have the same issues
        # with needing an existing Badge in order to be saved.
        old_save_m2m = getattr(self, 'save_m2m', lambda: None)

        def save_m2m():
            # Manually delete old entries
            model.badgelocale_set.all().delete()
            model.badgelocale_set = badge_locales

            old_save_m2m()

        if commit:
            model.save()
            save_m2m()
        else:
            self.save_m2m = save_m2m

        return model
