import json
from django.core.serializers import serialize, deserialize

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from banners.models import BannerImage


def mock_read(fieldfile):
    return 'CONTENT'


@patch('shared.serializers.json_files._read_fieldfile', mock_read)
class TestJSONFilesSerializer(TestCase):
    fixtures = ['serialize']

    def test_serialize_basic(self):
        """Test that files are serialized along with json data."""
        queryset = BannerImage.objects.all()
        results = json.loads(serialize('json_files', queryset))

        expected_files = {
            'uploads/banners/blue.png': 'CONTENT',
            'uploads/banners/green.png': 'CONTENT',
        }
        eq_(results['files'], expected_files)

        expected_json = json.loads(serialize('json', queryset))
        eq_(results['objects'], expected_json)

    @patch('shared.serializers.json_files._write_file')
    def test_deserialize_basic(self, _write_file):
        """Test that files are written to the filesystem on deserialization."""
        serialized_data = json.dumps({
            'files': {'file1.png': 'CONTENT', 'some/path': 'CONTENT'},
            'objects': []
        })

        list(deserialize('json_files', serialized_data))
        ok_((('file1.png', 'CONTENT'),) in _write_file.call_args_list)
        ok_((('some/path', 'CONTENT'),) in _write_file.call_args_list)
