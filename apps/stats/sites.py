from collections import defaultdict

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
            url(r'^stats/(?P<model_name>\w+)/$',
                self.admin_view(self.overview),
                name='stats.overview')
        )

        return my_patterns + urlpatterns

    def register_stats(self, model_class, stats_class):
        """Register a stats object with this admin site."""
        stat = stats_class(model_class, self)
        self.stats[stat.model_name] = stat

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        app_stats = defaultdict(list)
        for model_label, stat in self.stats.items():
            app_stats[stat.app_name].append(stat)
        extra_context.update({'app_stats': dict(app_stats)})

        return super(StatsAdminMixin, self).index(request, extra_context)

    def overview(self, request, model_name):
        if model_name not in self.stats.keys():
            raise Http404

        if request.method == 'POST':
            form = TimeSeriesSearchForm(request.POST)
            if form.is_valid():
                stat = self.stats[model_name]
                results = stat.data_for_period(
                    form.cleaned_data['start'], form.cleaned_data['end'],
                    form.cleaned_data['interval'])
        else:
            form = TimeSeriesSearchForm()
            results = None

        context = {'form': form, 'results': results}
        context_instance = RequestContext(request, current_app=self.name)
        return render_to_response(self.overview_template, context,
                                  context_instance=context_instance)
