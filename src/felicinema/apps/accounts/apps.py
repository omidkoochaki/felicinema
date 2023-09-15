from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # for translations uses


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'felicinema.apps.accounts'
    verbose_name = _("Accounts")
