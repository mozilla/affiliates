from django.db import models


class ModelStats:
    """Encapsulates options and functionality for displaying statistics for a
    given model.
    """
    datetime_field = None
    value_field = None

    def __init__(self, model, admin_site):
        self.model = model

        # If no datetime field is specified, use the first one found.
        if self.datetime_field is None:
            self.datetime_field = next(
                (field.name for field in model._meta.fields
                if isinstance(field, models.DateTimeField)), None)

    def get_urls(self):
        """Return urlpatterns for views associated with this object."""
        pass
