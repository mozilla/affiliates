from django.db import models

from qsstats import QuerySetStats


class ModelStats:
    """Encapsulates options and functionality for displaying statistics for a
    given model.
    """
    datetime_field = None
    aggregate = None

    def __init__(self, model, admin_site):
        self.model = model

        # If no datetime field is specified, use the first one found.
        if self.datetime_field is None:
            self.datetime_field = next(
                (field.name for field in model._meta.fields
                if isinstance(field, models.DateTimeField)), None)

    @property
    def admin_url(self):
        return '%s/%s' % ('stats', self.model_name)

    @property
    def model_name(self):
        return self.model._meta.object_name

    @property
    def app_name(self):
        return self.model._meta.app_label

    def data_for_period(self, start, end, interval='days'):
        """Return a time series of data for the given period."""
        qs = self.model.objects.all()
        qss = QuerySetStats(qs, self.datetime_field, aggregate=self.aggregate)
        return qss.time_series(start, end, interval=interval)
