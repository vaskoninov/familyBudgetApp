from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'familyBudgetApp.accounts'

    def ready(self):
        import familyBudgetApp.accounts.signals
