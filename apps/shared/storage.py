import os
from tempfile import mkstemp

from django.conf import settings
from django.core.files import locks
from django.core.files.move import file_move_safe
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename

class OverwritingStorage(FileSystemStorage):
    """
    File storage that allows overwriting of stored files.

    Modified from http://djangosnippets.org/snippets/2173/
    """

    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        """
        Lifted partially from django/core/files/storage.py
        """
        full_path = self.path(name)

        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # Ensure that content is open
        content.open()

        if hasattr(content, 'temporary_file_path'):
            # Content has a file that we can move.
            temp_data_location = content.temporary_file_path()
            file_move_safe(temp_data_location, full_path, allow_overwrite=True)
        else:
            # Write the content stream to a temporary file and move it.
            fd, tmp_path = mkstemp()
            locks.lock(fd, locks.LOCK_EX)
            for chunk in content.chunks():
                os.write(fd, chunk)
            locks.unlock(fd)
            os.close(fd)
            file_move_safe(tmp_path, full_path, allow_overwrite=True)

        content.close()
        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name
