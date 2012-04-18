from stats.sites import StatsAdminMixin


def patch(admin_site):
    """Monkeypatch admin site."""
    old_admin_class = admin_site.__class__
    admin_site.__class__ = type('StatsAdminSite',
                                (StatsAdminMixin, old_admin_class), {})
    admin_site._mixin_init()
