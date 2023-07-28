from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Account
# to get data from diff view
from transaction.models import Transaction
from users.models import Users
from books.models import *


def home(request):
    user_obj = Users.objects.filter(is_active=True)
    total_active_user = user_obj.count()
    available_book_obj = DB_Books.objects.filter(status=True)
    available_book_count = available_book_obj.count()
    borrowed_book_obj = DB_Books.objects.filter(status=False)
    borrowed_book_count = borrowed_book_obj.count()
    total_book = int(available_book_count) + int(borrowed_book_count)
    context = {'active_user_count': total_active_user, 'total_book': total_book,
               'available_book_count': available_book_count,
               'borrowed_book_count': borrowed_book_count}
    return render(request, 'home.html', context=context)


def index_view(request):
    return render(request, 'index.html')
