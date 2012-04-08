from django.db import models

from qsstats import QuerySetStats


class ModelStats:
    """Encapsulates options and functionality for displaying statistics for a
    given model.
    """
    display_name = None
    datetime_field = None
    aggregate = models.Count('id')

    def __init__(self, model, admin_site):
        self.model = model

        # If no datetime field is specified, use the first one found.
        if self.datetime_field is None:
            self.datetime_field = next(
                (field.name for field in model._meta.fields
                if isinstance(field, models.DateTimeField)), None)

    @property
    def slug(self):
        return '%s_%s' % (self.__class__.__name__, self.model_name)

    @property
    def name(self):
        return self.display_name or self.model_name

    @property
    def admin_url(self):
        return '%s/%s' % ('stats', self.slug)

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

    def aggregate_for_period(self, start, end):
        """Return the aggregate of all data for the given period."""
        qs = self.model.objects.all()
        date_filter = {'%s__range' % self.datetime_field: (start, end)}
        return qs.filter(**date_filter).aggregate(agg=self.aggregate)['agg']
