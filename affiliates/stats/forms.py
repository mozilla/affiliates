from django import forms


INTERVAL_CHOICES = [(k, k) for k in ('minutes', 'hours', 'days', 'weeks',
                                     'months', 'years')]


class StatsFilterForm(forms.Form):
    """Form for filtering the statistics shown in the admin interface ."""
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES)
