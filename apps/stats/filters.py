from collections import namedtuple
from urllib import urlencode

from django.contrib.admin.util import get_fields_from_path
from django.db import models
from django.template.loader import render_to_string


Choice = namedtuple('Choice', ['name', 'link', 'selected'])


class FilterSpec(object):
    """Encapsulates logic for showing a sidebar filter in the stats pages.

    Similar in concept to the django admin's FilterSpec, but simplified and not
    dependent on ChangeList or ModelAdmin.
    """

    def __init__(self, request, model, filter_name):
        self.request = request
        self.model = model
        self.field = get_fields_from_path(model, filter_name)[-1]
        self.name = filter_name
        self.type = None

        # Determine the filter type.
        # Relations
        if (hasattr(self.field, 'rel') and bool(self.field.rel) or
            isinstance(self.field, models.related.RelatedObject)):
            self.type = 'relation'

        # Boolean fields
        if (isinstance(self.field, models.BooleanField) or
            isinstance(self.field, models.NullBooleanField)):
            self.type = 'boolean'

        # Choice fields
        if bool(self.field.choices):
            self.type = 'choice'

        # Parse value
        value = self.request.GET.get(self.name, None)
        try:
            if self.type == 'relation':
                self.value = long(value)
            elif self.type == 'boolean':
                self.value = bool(value)
            else:
                self.value = value
        except (ValueError, TypeError):
            self.value = value

    @property
    def title(self):
        return self.field.verbose_name

    def apply_filter(self, qs):
        """Apply the filter if it appears in the request's query string."""
        if self.value is not None:
            filters = {self.name: self.value}
            qs = qs.filter(**filters)
        return qs

    def get_choices(self):
        """Return a list of choices for this filter based on the field type."""
        field_choices = [(None, 'All')]

        if self.type == 'relation':
            field_choices += self.field.get_choices(include_blank=False)
        elif self.type == 'boolean':
            field_choices += [(True, 'True'), (False, 'False')]
        elif self.type == 'choice':
            field_choices += self.field.flatchoices

        choices = [
            Choice(name, self._link(**{self.name: value}), self.value == value)
            for value, name in field_choices]

        return choices

    def _link(self, **kwargs):
        """Build a new link to the stats display with the specified filters.

        kwargs are added to the query string. If a kwargs has a value of None,
        it is removed from the query string.
        """
        path = self.request.path
        query = self.request.GET.copy()
        for key, value in kwargs.items():
            if value is None and key in query:
                del query[key]
            elif value is not None:
                query[key] = value

        return '%s?%s' % (path, urlencode(query))

    def has_output(self):
        choices = self.get_choices()
        return bool(choices)

    def output(self):
        context = {'title': self.title, 'choices': self.get_choices}
        return render_to_string('stats/filter.html', context)
