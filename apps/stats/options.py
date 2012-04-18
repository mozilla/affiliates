import json
from datetime import datetime, timedelta

from django.db import models
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse

from qsstats import QuerySetStats

from stats.filters import FilterSpec
from stats.forms import StatsFilterForm


class ModelStats:
    """Encapsulates options and functionality for displaying statistics for a
    given model.
    """
    aggregate = models.Count('id')
    datetime_field = None
    default_interval = 'days'
    display_name = None
    filters = []
    overview_template = 'stats/overview.html'
    qs = None

    def __init__(self, model, admin_site):
        self.model = model

        # If no queryset is specified, use all() on the registered model.
        if self.qs is None:
            self.qs = self.model.objects.all()

        # If no datetime field is specified, use the first one found.
        if self.datetime_field is None:
            self.datetime_field = next(
                (field.name for field in model._meta.fields
                if isinstance(field, models.DateTimeField)), None)

    @property
    def slug(self):
        return slugify('%s %s' % (self.__class__.__name__, self.name))

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

    def get_filters(self, request):
        """Get the set of FilterSpecs for this stat, if there are any.

        Returns a tuple of (filter_specs, has_filters).
        """
        filter_specs = [FilterSpec(request, self.model, filter_name)
                        for filter_name in self.filters]
        return filter_specs, bool(filter_specs)

    def data_for_period(self, qs, start, end, interval='days'):
        """Return a time series of data for the given period."""
        qss = QuerySetStats(qs, self.datetime_field,
                            aggregate=self.aggregate)
        return qss.time_series(start, end, interval=interval)

    def aggregate_for_period(self, qs, start, end):
        """Return the aggregate of all data for the given period."""
        date_filter = {'%s__range' % self.datetime_field: (start, end)}
        return qs.filter(**date_filter).aggregate(agg=self.aggregate)['agg']

    def default_start(self):
        """Generate the start date to use if no dates are specified."""
        return datetime.now() - timedelta(days=7)

    def default_end(self):
        """Generate the end date to use if no dates are specified."""
        return datetime.now()

    def overview(self, request):
        """Main display view for this statistic."""
        # TODO: Better handling of datetime minute, second, and hour.
        form = StatsFilterForm(request.GET)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            interval = form.cleaned_data['interval']
        else:
            start = self.default_start()
            end = self.default_end()
            interval = self.default_interval

        qs = self.qs
        filter_specs, has_filters = self.get_filters(request)
        for filter_spec in filter_specs:
            qs = filter_spec.apply_filter(qs)

        results = self.data_for_period(qs, start, end, interval)
        results_json = self.json_dumps(results)
        aggregate = self.aggregate_for_period(qs, start, end)


        context = {'title': self.name,
                   'form': form,
                   'results': results,
                   'results_json': results_json,
                   'aggregate': aggregate,
                   'filter_specs': filter_specs,
                   'has_filters': has_filters}
        return TemplateResponse(request, self.overview_template, context)

    def json_dumps(self, data):
        """Dumps the given data to a JSON string, including datetime objects."""
        # Handler courtesy of http://stackoverflow.com/q/455580
        def handler(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError, ('Object of type %s with value of %s is not '
                                  'JSON serializable' % (type(obj), repr(obj)))
        return json.dumps(data, default=handler)
