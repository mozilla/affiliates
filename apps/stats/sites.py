from collections import defaultdict


class StatsAdminMixin(object):
    index_template = 'stats/index.html'

    # These should be instance methods... but considering that there's
    # (usually) only one admin site object, I can live with this for now.
    stats = defaultdict(list)

    def get_urls(self):
        urlpatterns = super(StatsAdminMixin, self).get_urls()
        return urlpatterns

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        app_model_labels = {}
        for app_label, stats in self.stats.items():
            app_model_labels[app_label] = [stat.model._meta.object_name
                                           for stat in stats]
        extra_context.update({'app_model_labels': app_model_labels})

        return super(StatsAdminMixin, self).index(request, extra_context)

    def register_stats(self, model_class, stats_class):
        """Register a stats object with this admin site."""
        modelstats = stats_class(model_class, self)
        app = model_class._meta.app_label

        self.stats[app].append(modelstats)
