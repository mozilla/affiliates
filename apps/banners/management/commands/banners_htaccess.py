from os.path import join, dirname

from django.core.management.base import BaseCommand

from banners.utils import current_firefox_regexp
from settings import MEDIA_ROOT, BANNERS_HASH

CURRENT_PATH = dirname(__file__)


class Command(BaseCommand):
    help = 'Generate an .htaccess file for special banners to upgrade Firefox'

    def handle(self, *args, **options):
        template = open(join(CURRENT_PATH, 'htaccess.template')).read()

        banners_hash = '|'.join(BANNERS_HASH)

        version_regexp = current_firefox_regexp()

        output = template % (banners_hash, version_regexp)

        with open(join(MEDIA_ROOT, '.htaccess'), 'w') as f:
            f.write(output)
