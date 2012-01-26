"""Add all existing locales as enabled for all badges."""
try:
    from badges.models import Badge, BadgeLocale
    from shared.models import LANGUAGE_CHOICES

    abort = False
except ImportError:
    # BadgeLocale was removed by a subsequent commit, and causes an ImportError.
    # We can safely skip this in that case.
    abort = True


def run():
    if not abort:
        locales = [lang[0] for lang in LANGUAGE_CHOICES]

        for badge in Badge.objects.all():
            badge_locales = [BadgeLocale(badge=badge, locale=locale)
                             for locale in locales]
            badge.badgelocale_set.all().delete()
            badge.badgelocale_set = badge_locales
            badge.save()
