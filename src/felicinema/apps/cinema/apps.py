from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # for translations uses


class CinemaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'felicinema.apps.cinema'
    verbose_name = _('Events')
