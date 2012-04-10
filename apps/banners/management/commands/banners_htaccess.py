from os.path import join, dirname

from django.core.management.base import BaseCommand

from settings import MEDIA_ROOT
from product_details import product_details

BANNERS_HASH = (
    '5f5e8cc58fac3f658fca66be259590ea42963aa8',
#    'b6132eb3c1efeef2b25c93bc8bbee8b469d8d5b4',
)

CURRENT_PATH = dirname(__file__)


class Command(BaseCommand):
    help = 'Generate an .htaccess file for special banners to upgrade Firefox'

    def handle(self, *args, **options):
        template = open(join(CURRENT_PATH, 'htaccess.template')).read()

        banners_hash = '|'.join(BANNERS_HASH)

        current_firefox = int(product_details.firefox_versions['LATEST_FIREFOX_VERSION'].split('.')[0])
        versions = ['%s.*' % i for i in range(current_firefox, current_firefox + 4)]
        version_regexp = '|'.join(versions)

        output = template % (banners_hash, version_regexp)

        with open(join(MEDIA_ROOT, '.htaccess'), 'w') as f:
            f.write(output)
