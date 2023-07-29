from django.apps import AppConfig


class TransactionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transaction'

    # def ready(self):
    #     import transactions.signals  # Importing the signals module
    #     transactions.signals.register_signals()  # Register signals defined in the signals.py module