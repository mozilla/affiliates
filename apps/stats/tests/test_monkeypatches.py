from django.contrib.admin.sites import AdminSite

from mock import patch
from nose.tools import eq_

from shared.tests import TestCase
from stats.monkeypatches import patch as patch_admin
from stats.sites import StatsAdminMixin


class PatchTests(TestCase):
    @patch.object(StatsAdminMixin, '_mixin_init')
    def test_patch_mixin_init(self, _mixin_init):
        """Test that patching an admin site calls _mixin_init."""
        eq_(_mixin_init.called, False)
        admin_site = AdminSite()
        patch_admin(admin_site)
        eq_(_mixin_init.called, True)
