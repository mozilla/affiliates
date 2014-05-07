from django.template.loader import render_to_string

from jingo import register
from jinja2 import Markup

from affiliates.links.models import LeaderboardStanding


@register.function
def leaderboard(metric='link_clicks', count=5):
    """Display a leaderboard of the top ranked users."""
    standings = (LeaderboardStanding.objects
                 .filter(metric=metric)
                 .select_related('user', 'user__userprofile')
                 .order_by('ranking')[:count])
    return Markup(render_to_string('links/widgets/leaderboard.html', {'standings': standings}))
