import os.path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from product_details import product_details

from affiliates.banners.models import FirefoxUpgradeBannerVariation


class Command(BaseCommand):
    help = ('Generate .htaccess for the media directory for smart banners.')

    def handle(self, *args, **kwargs):
        print 'Generating new .htaccess...'

        try:
            current_version = product_details.firefox_versions['LATEST_FIREFOX_VERSION']
            current_version_int = int(current_version.split('.')[0])
        except (AttributeError, KeyError) as e:
            raise CommandError('Could not retrieve latest version from product details: ', e)
        except ValueError:
            raise CommandError('Could not parse version string: ' + current_version)

        version_range = range(current_version_int, current_version_int + 4)
        version_regex = '|'.join(unicode(version) for version in version_range)
        variations = FirefoxUpgradeBannerVariation.objects.all()

        htaccess = render_to_string('banners/media.htaccess', {
            'version_regex': version_regex,
            'upgrade_banner_variations': variations
        })

        with open(os.path.join(settings.MEDIA_ROOT, '.htaccess'), 'w') as f:
            f.write(htaccess)

        print 'Done!'
