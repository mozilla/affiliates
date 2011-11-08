from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from funfactory.admin import site
from badges.models import Category, Subcategory, BadgeLocale


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

        # Manually delete old entries
        model.badgelocale_set.all().delete()
        model.badgelocale_set = badge_locales

        if commit:
            model.save()

        return model


class CategoryAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'
site.register(Subcategory, SubcategoryAdmin)
