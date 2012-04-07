from funfactory import admin

from stats.sites import StatsAdminMixin


# TODO: Do this for the built in admin instead.
def patch():
    """Monkeypatch admin site."""
    old_admin_class = admin.site.__class__
    admin.site.__class__ = type('StatsAdminSite',
                                (StatsAdminMixin, old_admin_class), {})
