from django.shortcuts import render, redirect
from .models import Transaction
from users.models import Users
from books.models import *
from django.db.models import Q
from django.contrib import messages
from django.core import serializers
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
# from accounts.models import Account
from django.contrib.auth.decorators import login_required

# Create your views here.


def transaction(request):
    borrow_transaction_obj = Transaction.objects.filter(is_returned=False, date_added__date=timezone.now().date()).order_by('-date_added')
    return_transaction_obj = Transaction.objects.filter(is_returned=True, return_date__date=timezone.now().date()).order_by('-date_added')

    context = {'borrow_transaction_obj': borrow_transaction_obj, 'return_transaction_obj': return_transaction_obj}
    return render(request, 'transactions/transaction.html', context)


def fetch_user_info(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        # search_user = Q(phone_number__contains=search_str)
        user_obj = Users.objects.filter(phone_number=search_str)
        data = user_obj.values()
        if user_obj.exists():
            # messages.success(request, f'Record Found for: {search_str}')
            return JsonResponse(list(data), safe=False)
        else:
            # messages.error(request, f'No records found for the query: {search_str}')
            return JsonResponse(list(data), safe=False)


def fetch_book_info(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        # search_user = Q(phone_number__contains=search_str)
        book_obj = DB_Books.objects.filter(book_id=search_str)
        # data = book_obj.values()
        data = book_obj.values('book_id', 'book_title', 'book_author_id', 'book_author__name', 'book_language')
        if book_obj.exists():
            return JsonResponse(list(data), safe=False)
        else:
            return JsonResponse(list(data), safe=False)


def borrow_book_old(request):
    if request.method == 'POST':
        phone_number = request.POST.get('user_phone_number_data')
        book_id = request.POST.get('book_id_data')

        # Get book object to update book status to False
        book_obj = DB_Books.objects.get(book_id=book_id)
        book_obj.status = False
        book_obj.save()
        # Retrieve the Users instance based on the user_id
        user_instance = get_object_or_404(Users, phone_number=phone_number)
        book_instance = get_object_or_404(DB_Books, book_id=book_id)
        transaction_obj = Transaction(user=user_instance, book=book_instance)
        transaction_obj.save()
        messages.success(request, f'Borrowing {book_id}\' record added successfully!')
        borrow_transaction_obj = Transaction.objects.filter(is_returned=False, date_added__date=timezone.now().date()).order_by('-date_added')
        return_transaction_obj = Transaction.objects.filter(is_returned=True, return_date__date=timezone.now().date()).order_by('-date_added')

        context = {'borrow_transaction_obj': borrow_transaction_obj, 'return_transaction_obj': return_transaction_obj}
        return render(request, 'transactions/transaction.html', context)
    elif request.method == 'GET':
        # Handle the GET request and retrieve the transaction objects
        borrow_transaction_obj = Transaction.objects.filter(is_returned=False,
                                                            date_added__date=timezone.now().date()).order_by(
            '-date_added')
        return_transaction_obj = Transaction.objects.filter(is_returned=True,
                                                            return_date__date=timezone.now().date()).order_by(
            '-date_added')

        context = {'borrow_transaction_obj': borrow_transaction_obj, 'return_transaction_obj': return_transaction_obj}
        return render(request, 'transactions/borrow_book.html', context)


@login_required
def return_book(request):
    if request.method == 'POST':

        book_id = request.POST.get('book_id_data')

        book_instance = get_object_or_404(DB_Books, book_id=book_id)
        # need to check qr code file is updating or creating new one
        book_obj = DB_Books.objects.get(book_id=book_id)
        book_obj.status = True
        book_obj.save()
        try:
            return_transaction_obj = Transaction.objects.get(book=book_instance, is_returned=False)

            # # update user book_borrowed_status = False
            user_obj = Users.objects.get(phone_number=return_transaction_obj.user.phone_number)
            user_obj.number_of_books_borrowed -= 1
            user_obj.save()

            return_transaction_obj.is_returned = True
            return_transaction_obj.return_date = timezone.now()
            # Get Login librarian first name
            return_transaction_obj.librarian_name = request.user.first_name

            return_transaction_obj.save()
            messages.success(request, f'Return book {book_id}\' record Updated successfully!')
            borrow_transaction_obj = Transaction.objects.filter(is_returned=False,
                                                                date_added__date=timezone.now().date()).order_by('-date_added')
            return_transaction_obj = Transaction.objects.filter(is_returned=True, return_date__date=timezone.now().date()).order_by('-date_added')

            context = {'borrow_transaction_obj': borrow_transaction_obj,
                       'return_transaction_obj': return_transaction_obj}
            return render(request, 'transactions/transaction.html', context)
        except Transaction.DoesNotExist:
            messages.error(request, f'Book you scanned is not borrowed Please re check Book ID{book_id}.')
            return render(request, 'transactions/return_book.html')

    return render(request, 'transactions/return_book.html')

@login_required
def borrow_book(request):
    if request.method == 'POST':
        phone_number = request.POST.get('user_phone_number_data')
        book_id = request.POST.get('book_id_data')

        # Your borrowing logic and form processing here...
        try:
            book_obj = DB_Books.objects.get(book_id=book_id, status=True)
        except DB_Books.DoesNotExist:
            messages.error(request, f'Book with ID {book_id} does not exist. Its already borrowed 1st return it then borrow')
            return redirect('borrow_book')  # Redirect back to the borrowing form

        # Update book status and save transaction
        book_obj.status = False
        book_obj.save()

        # Retrieve the Users instance based on the phone_number
        user_instance = get_object_or_404(Users, phone_number=phone_number)
        book_instance = get_object_or_404(DB_Books, book_id=book_id)
        transaction_obj = Transaction(user=user_instance, book=book_instance)
        transaction_obj.transaction_type = 'borrow'
        # Get Login librarian first name
        transaction_obj.librarian_name = request.user.first_name
        transaction_obj.save()
        #update user borrowed book count
        user_obj = Users.objects.get(phone_number=phone_number)
        user_obj.number_of_books_borrowed += 1
        user_obj.save()

        # Redirect to transaction page after successful form submission
        messages.info(request, f'Borrowing {book_id}\'s record added successfully!')
        return redirect('transaction')

    elif request.method == 'GET':
        # Handle the GET request and retrieve the transaction objects
        borrow_transaction_obj = Transaction.objects.filter(is_returned=False,
                                                            date_added__date=timezone.now().date()).order_by(
            '-date_added')
        return_transaction_obj = Transaction.objects.filter(is_returned=True,
                                                            return_date__date=timezone.now().date()).order_by(
            '-date_added')

        context = {'borrow_transaction_obj': borrow_transaction_obj, 'return_transaction_obj': return_transaction_obj}
        return render(request, 'transactions/borrow_book.html', context)