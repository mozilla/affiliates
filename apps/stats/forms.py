from django import forms


INTERVAL_CHOICES = [(k, k) for k in ('minutes', 'hours', 'days', 'weeks',
                                     'months', 'years')]


class TimeSeriesSearchForm(forms.Form):
    """Form for searching for a time series of data."""
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES)
