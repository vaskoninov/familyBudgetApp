from django.apps import AppConfig


class BudgetAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'familyBudgetApp.budgetApp'

    def ready(self):
        import familyBudgetApp.budgetApp.signals
