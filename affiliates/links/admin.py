from affiliates.base.admin import admin_site, BaseModelAdmin
from affiliates.links.models import Link


class LinkAdmin(BaseModelAdmin):
    list_display = ('banner', 'banner_type', 'banner_variation', 'user_name', 'user_email',
                    'link_clicks', 'created')
    search_fields = ('id', 'user__userprofile__display_name', 'user__email')

    def user_name(self, link):
        return link.user.display_name

    def user_email(self, link):
        return link.user.email

    def banner_type(self, link):
        if link.is_image_link:
            return 'Image Link'
        elif link.is_text_link:
            return 'Text Link'
        elif link.is_upgrade_link:
            return 'Upgrade Link'
        else:
            return 'Unknown'

    def banner_variation(self, link):
        return link.banner_variation
    banner_variation.allow_tags = True


admin_site.register(Link, LinkAdmin)
