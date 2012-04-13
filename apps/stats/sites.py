from collections import defaultdict

from django.http import Http404


class StatsAdminMixin(object):
    index_template = 'stats/index.html'

    # These should be instance methods... but considering that there's
    # (usually) only one admin site object, I can live with this for now.
    stats = {}

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = super(StatsAdminMixin, self).get_urls()
        my_patterns = patterns('',
            url(r'^stats/(?P<stat_slug>[-\w]+)/$',
                self.admin_view(self.overview),
                name='stats.overview')
        )

        return my_patterns + urlpatterns

    def register_stats(self, model_class, stats_class):
        """Register a stats object with this admin site."""
        stat = stats_class(model_class, self)
        self.stats[self._find_unique_slug(stat.slug)] = stat

    def _find_unique_slug(self, slug):
        """Generates a unique stat slug that isn't taken by an existing stat."""
        new_slug = slug
        affix = 1
        while True:
            if new_slug not in self.stats.keys():
                return new_slug
            else:
                slug = new_slug.append(affix)
                affix += 1

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        app_stats = defaultdict(list)
        for model_label, stat in self.stats.items():
            app_stats[stat.app_name].append(stat)
        extra_context.update({'app_stats': dict(app_stats)})

        return super(StatsAdminMixin, self).index(request, extra_context)

    def overview(self, request, stat_slug):
        """Routes overview view to specified ModelStat."""
        if stat_slug not in self.stats.keys():
            raise Http404
        stat = self.stats[stat_slug]
        return stat.overview(request)
