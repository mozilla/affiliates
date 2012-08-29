from django.contrib.admin import ModelAdmin
from django.db import models

from form_utils.widgets import ImageWidget

from shared.forms import AdminModelForm


class BaseModelAdmin(ModelAdmin):
    """Base class for ModelAdmins used across the site."""
    form = AdminModelForm
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}
