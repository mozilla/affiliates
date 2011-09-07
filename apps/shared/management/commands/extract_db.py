import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model

from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from tower.management.commands.extract import TEXT_DOMAIN, tweak_message


class Command(BaseCommand):
    """
    Pulls strings from the database and appends them to an existing pot file.

    The models and attributes to pull are defined by DB_LOCALIZE:

    DB_LOCALIZE = {
        'some_app': {
            SomeModel': {
                'attrs': ['attr_name', 'another_attr'],
            }
        },
        'another_app': {
            AnotherModel': {
                'attrs': ['more_attrs'],
                'comments': ['Comment that will appear to localizers.'],
            }
        },
    }

    Database columns are expected to be CharFields or TextFields.
    """
    help = ('Pulls strings from the database and appends them to an existing '
            '.pot file.')
    option_list = BaseCommand.option_list + (
        make_option('--output-dir', '-o',
                    default=os.path.join(settings.ROOT, 'locale', 'templates',
                                         'LC_MESSAGES'),
                    dest='outputdir',
                    help='The directory where extracted files are located.'
                         '(Default: %default)'),
        )

    def handle(self, *args, **options):
        try:
            apps = settings.DB_LOCALIZE
        except AttributeError:
            raise CommandError('DB_LOCALIZE setting is not defined!')

        strings = []
        # Oh god this is terrible
        for app, models in apps.items():
            for model, params in models.items():
                model_class = get_model(app, model)
                for item in model_class.objects.all().values():
                    for attr in params['attrs']:
                        msg = {
                            'id': item[attr],
                            'auto_comments': ['DB: %s.%s.%s' %
                                              (app, model, attr)],
                            'user_comments': params['comments'],
                            }
                        strings.append(msg)

        po_dir = os.path.abspath(options.get('outputdir'))
        po_filename = os.path.join(po_dir, '%s.pot' % TEXT_DOMAIN)

        try:
            with open(po_filename, 'r') as f:
                catalog = read_po(f)
        except IOError:
            catalog = Catalog()

        for msg in strings:
            catalog.add(tweak_message(msg['id']),
                        auto_comments=msg['auto_comments'],
                        user_comments=msg['user_comments'])

        with open(po_filename, 'w+') as f:
            write_po(f, catalog)
