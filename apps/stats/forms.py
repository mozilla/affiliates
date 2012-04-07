from datetime import datetime, timedelta

from django import forms


INTERVAL_CHOICES = [(k, k) for k in ('minutes', 'hours', 'days', 'weeks',
                                     'months', 'years')]


class TimeSeriesSearchForm(forms.Form):
    """Form for searching for a time series of data."""
    start = forms.DateTimeField(
        initial=lambda: datetime.now() - timedelta(days=7))
    end = forms.DateTimeField(initial=datetime.now)
    interval = forms.ChoiceField(initial='days',
                                 choices=INTERVAL_CHOICES)
