from funfactory.admin import site

from facebook.forms import FacebookBannerAdminForm
from facebook.models import FacebookBanner, FacebookBannerLocale
from shared.admin import BaseModelAdmin


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
