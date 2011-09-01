import os

from django.conf import settings
from django.core import management

from babel.messages.pofile import read_po
from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase
from tower.management.commands.extract import TEXT_DOMAIN


DB_LOCALIZE = {
    'badges': {
        'Category': {
            'comments': ['Category of badges to choose from.'],
            'attrs': ['name']
        }
    }
}


@patch.object(settings, 'DB_LOCALIZE', DB_LOCALIZE)
class ExtractDBTests(TestCase):
    fixtures = ['db_localize']

    def test_basic(self):
        output_dir = os.path.join(settings.ROOT, 'tmp')
        output_file = os.path.join(os.path.abspath(output_dir),
                                   '%s.pot' % TEXT_DOMAIN)

        try:
            os.remove(output_file)
        except OSError:
            pass  # File doesn't exist, which is fine

        management.call_command('extract_db', outputdir=output_dir)
        with open(output_file, 'r') as f:
            potfile = read_po(f)

        msg = potfile['Localize String']
        ok_(msg is not None)
        eq_(msg.user_comments, DB_LOCALIZE['badges']['Category']['comments'])
