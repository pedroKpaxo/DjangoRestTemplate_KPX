from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestauthConfig(AppConfig):
    name = 'apps.restauth'
    verbose_name = _("Restauths")
