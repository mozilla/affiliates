import os
from os.path import join, dirname

from django.conf import settings
from django.core.management.base import BaseCommand

from affiliates.banners.utils import current_firefox_regexp


CURRENT_PATH = dirname(__file__)


class Command(BaseCommand):
    help = 'Generate an .htaccess file for special banners to upgrade Firefox'

    def handle(self, *args, **options):
        # If there are no special banners to handle, remove the .htaccess.
        if not settings.BANNERS_HASH:
            try:
                os.remove(join(settings.MEDIA_ROOT, '.htaccess'))
            except OSError:
                pass  # File did not exist, this is fine.
        else:
            template = open(join(CURRENT_PATH, 'htaccess.template')).read()
            banners_hash = '|'.join(settings.BANNERS_HASH)
            version_regexp = current_firefox_regexp()
            output = template % (banners_hash, version_regexp)

            with open(join(settings.MEDIA_ROOT, '.htaccess'), 'w') as f:
                f.write(output)
