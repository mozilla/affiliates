from django.contrib.admin import ModelAdmin

from shared.forms import AdminModelForm


class BaseModelAdmin(ModelAdmin):
    """Base class for ModelAdmins used across the site."""
    form = AdminModelForm
