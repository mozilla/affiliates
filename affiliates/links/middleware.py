from datetime import timedelta

from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone

from tower import ugettext_lazy as _lazy

from affiliates.links.models import DataPoint
from affiliates.users.models import UserProfile

class StatsSinceLastVisitMiddleware(object):
    """
    If new data has been collected since the user's last visit, display
    a message showing the data.
    """
    # L10n: "Woot" (w00t) as in internet slang expressing happiness.
    message_string = _lazy('Woot! You\'ve driven {num_downloads} downloads and {num_clicks} '
                           'clicks since your last visit. Keep rockin\'!')

    def process_request(self, request):
        # Ignore unauthed users.
        if not request.user.is_authenticated():
            return None

        # Ignore FacebookUsers (who don't have a profile) or users
        # without a profile in the database.
        try:
            profile = request.user.userprofile
        except (AttributeError, UserProfile.DoesNotExist):
            return None

        # Ignore users that haven't visited before or visited recently.
        now = timezone.now().date()
        if not profile.last_visit:
            profile.last_visit = now
            profile.save()
            return None
        elif now - profile.last_visit < timedelta(days=1):
            return None

        # Show a message if there were clicks or downloads.
        datapoints = DataPoint.objects.filter(link__user=request.user,
                                              date__gt=profile.last_visit, date__lte=now)
        totals = datapoints.aggregate(num_clicks=Sum('link_clicks'),
                                      num_downloads=Sum('firefox_downloads'))
        if totals['num_clicks'] or totals['num_downloads']:
                messages.info(request, unicode(self.message_string).format(**totals))

        # Update their last visit date.
        profile.last_visit = now
        profile.save()
        return None
