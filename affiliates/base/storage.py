from django.core.files.storage import FileSystemStorage


class OverwritingStorage(FileSystemStorage):
    """
    Taken from https://djangosnippets.org/snippets/976/.
    """

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        if self.exists(name):
            self.delete(name)
        return name
