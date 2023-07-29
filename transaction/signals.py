# transactions/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, TransactionHistory


@receiver(post_save, sender=Transaction)
def update_transaction_history(sender, instance, **kwargs):
    # Your signal handling logic here, e.g., creating/updating TransactionHistory objects
    # based on the changes to the Transaction model
    pass


def register_signals():
    # Connect your signal handlers here
    post_save.connect(update_transaction_history, sender=Transaction)
