from django.contrib import admin
from .models import Transaction

# admin.site.register(Transaction)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'book_id', 'book_title', 'user_name', 'user_phone', 'borrow_date', 'return_date',
                    'is_returned', 'date_added')

    def book_id(self, obj):
        return obj.book.book_id

    def book_title(self, obj):
        return obj.book.book_title

    def user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def user_phone(self, obj):
        return obj.user.phone_number

    book_id.short_description = 'Book ID'
    book_title.short_description = 'Book Title'
    user_name.short_description = 'User Name'
    user_phone.short_description = 'User Phone'


# Register the Transaction model with the custom admin class
admin.site.register(Transaction, TransactionAdmin)
