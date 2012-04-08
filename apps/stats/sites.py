import json
from collections import defaultdict
from datetime import datetime, timedelta

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stats.forms import TimeSeriesSearchForm


class StatsAdminMixin(object):
    index_template = 'stats/index.html'
    overview_template = 'stats/overview.html'

    # These should be instance methods... but considering that there's
    # (usually) only one admin site object, I can live with this for now.
    stats = {}

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = super(StatsAdminMixin, self).get_urls()
        my_patterns = patterns('',
            url(r'^stats/(?P<stat_slug>\w+)/$',
                self.admin_view(self.overview),
                name='stats.overview')
        )

        return my_patterns + urlpatterns

    def register_stats(self, model_class, stats_class):
        """Register a stats object with this admin site."""
        stat = stats_class(model_class, self)
        self.stats[stat.slug] = stat

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        app_stats = defaultdict(list)
        for model_label, stat in self.stats.items():
            app_stats[stat.app_name].append(stat)
        extra_context.update({'app_stats': dict(app_stats)})

        return super(StatsAdminMixin, self).index(request, extra_context)

    def overview(self, request, stat_slug):
        if stat_slug not in self.stats.keys():
            raise Http404
        stat = self.stats[stat_slug]

        if request.method == 'POST':
            form = TimeSeriesSearchForm(request.POST)
        else:
            form = TimeSeriesSearchForm({
                'start': datetime.now() - timedelta(days=7),
                'end': datetime.now(),
                'interval': 'days'
            })

        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            interval = form.cleaned_data['interval']

            results = stat.data_for_period(start, end, interval)
            results_json = self.json_dumps(results)
            aggregate = stat.aggregate_for_period(start, end)
        else:
            results = None
            results_json = None
            aggregate = None

        context = {'form': form,
                   'results': results,
                   'results_json': results_json,
                   'aggregate': aggregate,
                   'title': stat.name}
        context_instance = RequestContext(request, current_app=self.name)
        return render_to_response(self.overview_template, context,
                                  context_instance=context_instance)

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
