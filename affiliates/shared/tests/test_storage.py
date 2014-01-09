# Taken from http://djangosnippets.org/snippets/2173/

import shutil
import tempfile

from django.core.files.base import ContentFile as C
from django.core.files import File
from nose.tools import assert_raises, eq_

from affiliates.shared.storage import OverwritingStorage
from affiliates.shared.tests import TestCase

class TestOverwritingStorage(TestCase):
    def setUp(self):
        self.location = tempfile.mkdtemp(prefix="overwriting_storage_test")
        self.storage = OverwritingStorage(location=self.location)

    def tearDown(self):
        shutil.rmtree(self.location)

    def test_new_file(self):
        s = self.storage
        assert not s.exists("foo")
        s.save("foo", C("new"))
        eq_(s.open("foo").read(), "new")

    def test_overwriting_existing_file_with_string(self):
        s = self.storage

        s.save("foo", C("old"))
        name = s.save("foo", C("new"))
        eq_(s.open("foo").read(), "new")
        eq_(name, "foo")

    def test_overwrite_with_file(self):
        s = self.storage

        input_file = s.location + "/input_file"
        with open(input_file, "w") as input:
            input.write("new")

        s.save("foo", C("old"))
        name = s.save("foo", File(open(input_file)))

        eq_(s.open("foo").read(), "new")
        eq_(name, "foo")

    def test_upload_fails(self):
        s = self.storage

        class Explosion(Exception):
            pass

        class ExplodingContentFile(C):
            def __init__(self):
                super(ExplodingContentFile, self).__init__("")

            def chunks(self):
                yield "bad chunk"
                raise Explosion("explode!")

        s.save("foo", C("old"))

        assert_raises(Explosion, s.save, 'foo', ExplodingContentFile())
        eq_(s.open("foo").read(), "old")
