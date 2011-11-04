"""
Serializer that includes files from FileFields as part of the serialized data.
"""
import os
from base64 import b64decode, b64encode
from StringIO import StringIO

import django.core.serializers.json as json_s
import django.core.serializers.python as python_s
from django.conf import settings
from django.db.models import FileField
from django.utils import simplejson


class Serializer(json_s.Serializer):
    """Convert a queryset to JSON, and add data for FileField files."""
    def __init__(self, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)

        self.files = {}

    def end_serialization(self):
        data = {
            'files': self.files,
            'objects': self.objects
        }
        simplejson.dump(data, self.stream, cls=json_s.DjangoJSONEncoder,
                        **self.options)

    def handle_field(self, obj, field):
        """Serialize field."""
        if isinstance(field, FileField):
            file = getattr(obj, field.name)
            self.files[file.name] = _read_fieldfile(file)

        super(Serializer, self).handle_field(obj, field)


def Deserializer(stream_or_string, **options):
    """Deserialize a string or stream of JSON data with files embedded."""
    if isinstance(stream_or_string, basestring):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string

    data = simplejson.load(stream)
    for name, file_data in data['files'].items():
        _write_file(name, file_data)

    for obj in python_s.Deserializer(data['objects']):
        yield obj


def _read_fieldfile(fieldfile):
    """Reads a fieldfile and encodes it. Mocked in tests."""
    with fieldfile as file:
        file.open('r')
        data = b64encode(file.read())

    return data


def _write_file(name, data):
    """Write file to filesystem. Mocked in tests."""
    with open(os.path.join(settings.MEDIA_ROOT, name), 'w') as file:
        file.write(b64decode(data))
