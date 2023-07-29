from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from books.models import DB_Books
from users.models import Users


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(DB_Books, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)
    librarian_name = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'Transaction ID: {self.transaction_id} - User: {self.user.phone_number} - Book: {self.book.book_id}'

    def save(self, *args, **kwargs):
        if self.is_returned and not self.return_date:
            self.return_date = timezone.now()
            # self.book.no_of_copies_current += 1  # Increment the number of copies
        elif not self.is_returned:
            pass
            # self.book.no_of_copies_current -= 1  # Decrement the number of copies
        # self.book.save()
        super().save(*args, **kwargs)

#
# class TransactionHistory(models.Model):
#     transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
#     operation = models.CharField(max_length=20)  # 'borrow' or 'return'
#     timestamp = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f'Transaction ID: {self.transaction.transaction_id} - Operation: {self.operation}'
#
#
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
#
#
# @receiver(post_save, sender=Transaction)
# def create_transaction_history_on_save(sender, instance, created, **kwargs):
#     operation = 'borrow' if instance.is_returned else 'return'
#     TransactionHistory.objects.create(transaction=instance, operation=operation)
#
#
# @receiver(post_delete, sender=Transaction)
# def create_transaction_history_on_delete(sender, instance, **kwargs):
#     operation = 'borrow' if instance.is_returned else 'return'
#     TransactionHistory.objects.create(transaction=instance, operation=f'delete_{operation}')
