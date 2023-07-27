from django.urls import path
from . import views

urlpatterns = [ path('managebook/', views.managebook, name='managebook'),
                path('add_book/', views.add_book, name='add_book'),
                path('edit_book/', views.edit_book, name='edit_book'),
                path('update_book/<str:id>', views.update_book, name='update_book'),
                path('delete_book/<str:id>', views.delete_book, name='delete_book'),
                path('view_book/', views.view_book, name='view_book'),
                path('view_bookqrcode/', views.view_bookqrcode, name='view_bookqrcode'),
                # path('search_book/', views.search_book, name='search_book'),
                #category
                path('managecategory/', views.managecategory, name='managecategory'),
                path('add_category/', views.add_category, name='add_category'),
                path('edit_category/', views.edit_category, name='edit_category'),
                path('update_category/<str:id>', views.update_category, name='update_category'),
                path('view_category/', views.view_category, name='view_category'),
                path('delete_category/<str:id>', views.delete_category, name='delete_category'),
                # path('search_category/<str:id>', views.search_category, name='search_category'),
                #subcategory
                path('managesubcategory/', views.managesubcategory, name='managesubcategory'),
                path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
                path('edit_subcategory/', views.edit_subcategory, name='edit_subcategory'),
                path('update_subcategory/<str:id>', views.update_subcategory, name='update_subcategory'),
                path('view_subcategory/', views.view_subcategory, name='view_subcategory'),
                path('delete_subcategory/<str:id>', views.delete_subcategory, name='delete_subcategory'),
                # path('search_category/<str:id>', views.search_category, name='search_category'),

              ]
