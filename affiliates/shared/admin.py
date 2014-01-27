from django.contrib.admin import ModelAdmin
from django.db import models

from form_utils.widgets import ImageWidget
from funfactory.admin import SessionCsrfAdminSite

from affiliates.shared.forms import AdminModelForm


class AffiliatesAdminSite(SessionCsrfAdminSite):
    pass


class BaseModelAdmin(ModelAdmin):
    """Base class for ModelAdmins used across the site."""
    form = AdminModelForm
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}


admin_site = AffiliatesAdminSite()
