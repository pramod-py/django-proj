from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
                path('transaction/', views.transaction, name='transaction'),
                path('borrow_book/', views.borrow_book, name='borrow_book'),
                path('return_book/', views.return_book, name='return_book'),
                path('fetch_user_info/', csrf_exempt(views.fetch_user_info), name='fetch_user_info'),
                path('fetch_book_info/', csrf_exempt(views.fetch_book_info), name='fetch_book_info'),

              ]