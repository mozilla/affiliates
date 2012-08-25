from django.conf import settings
from django.contrib.admin.filterspecs import FilterSpec
from django.db import models

from form_utils.widgets import ImageWidget
from funfactory.admin import site

from facebook.forms import FacebookBannerAdminForm
from facebook.models import (FacebookBanner, FacebookBannerInstance,
                             FacebookBannerLocale)
from shared.admin import BaseModelAdmin


class TotalClicksGoalFilterSpec(FilterSpec):
    """
    Admin FilterSpec that filters by whether an IntegerField is past the click
    goal for becoming a Facebook ad.

    This is deep magic.
    """
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(TotalClicksGoalFilterSpec, self).__init__(
            f, request, params, model, model_admin, field_path=field_path)

        self.lookup_kwarg_gte = '%s__gte' % self.field_path
        self.lookup_kwarg_lt = '%s__lt' % self.field_path
        self.lookup_val_gte = (request.GET.get(self.lookup_kwarg_gte, None)
                               is not None)
        self.lookup_val_lt = (request.GET.get(self.lookup_kwarg_lt, None)
                              is not None)

    def title(self):
        return 'Met Click Goal (more than %s clicks)' % settings.FACEBOOK_CLICK_GOAL

    def choices(self, cl):
        """
        Yield possible choices for filter sidebar and how they affect the query
        string.
        """
        # TODO: Determine if non-static choices would be cleaner here.
        # Honestly, I tried a more generic version and it was even harder to
        # follow than this version.
        yield {
            'selected': not (self.lookup_val_gte or self.lookup_val_lt),
            'query_string': cl.get_query_string({}, [self.lookup_kwarg_gte,
                                                     self.lookup_kwarg_lt]),
            'display': 'All'
        }

        goal = settings.FACEBOOK_CLICK_GOAL
        yield {
            'selected': self.lookup_val_gte and not self.lookup_val_lt,
            'query_string': cl.get_query_string({self.lookup_kwarg_gte: goal},
                                                [self.lookup_kwarg_lt]),
            'display': 'Yes'
        }
        yield {
            'selected': self.lookup_val_lt and not self.lookup_val_gte,
            'query_string': cl.get_query_string({self.lookup_kwarg_lt: goal},
                                                [self.lookup_kwarg_gte]),
            'display': 'No'
        }
# Insert manually at the front of the list to be tested prior to the
# AllValuesFilterSpec catchall filter.
FilterSpec.filter_specs.insert(0, (
    lambda f: getattr(f, 'total_clicks_goal', False),
    TotalClicksGoalFilterSpec)
)


class FacebookBannerAdmin(BaseModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)
    form = FacebookBannerAdminForm

    def save_model(self, request, obj, form, change):
        """Save locale changes as well as the banner itself."""
        super(FacebookBannerAdmin, self).save_model(request, obj, form, change)

        locales = form.cleaned_data['locales']
        obj.locale_set.all().delete()
        for locale in locales:
            FacebookBannerLocale.objects.create(banner=obj, locale=locale)
site.register(FacebookBanner, FacebookBannerAdmin)


class FacebookBannerInstanceAdmin(BaseModelAdmin):
    list_display = ('text', 'banner', 'user', 'can_be_an_ad',
                    'use_profile_image', 'created', 'total_clicks',
                    'review_status')
    search_fields = ('text', 'banner__name', 'user__full_name')
    list_filter = ('banner', 'created', 'processed', 'review_status',
                   'total_clicks')
    readonly_fields = ('created', 'total_clicks')
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}
    fieldsets = (
        (None, {
            'fields': ('user', 'banner', 'text', 'created',
                       'total_clicks')
        }),
        ('Ad Review', {
            'fields': ('can_be_an_ad', 'review_status', 'custom_image')
        }),
        ('Advanced', {
            'fields': ('processed',),
            'classes': ('collapse',)
        }),
    )

    def use_profile_image(self, instance):
        return bool(instance.custom_image)
    use_profile_image.boolean = True
site.register(FacebookBannerInstance, FacebookBannerInstanceAdmin)
