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

    def __str__(self):
        return f'Transaction ID: {self.transaction_id} - User: {self.user.phone_number} - Book: {self.book.book_id}'

    def save(self, *args, **kwargs):
        if self.is_returned and not self.return_date:
            self.return_date = timezone.now()
            self.book.no_of_copies_current += 1  # Increment the number of copies
        elif not self.is_returned:
            self.book.no_of_copies_current -= 1  # Decrement the number of copies
        self.book.save()
        super().save(*args, **kwargs)