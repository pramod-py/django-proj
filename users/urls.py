from django.urls import path
from . import views

urlpatterns = [ path('manageuser/', views.manageuser, name='manageuser'),
                path('adduser/', views.adduser, name='adduser'),
                path('edituser/', views.edituser, name='edituser'),
                path('updateuser/<str:id>', views.updateuser, name='updateuser'),
                path('deleteuser/<str:id>', views.deleteuser, name='deleteuser'),
                path('viewuser/', views.viewuser, name='viewuser'),
                path('viewuserqrcode/', views.viewuserqrcode, name='viewuserqrcode'),
                path('searchuser/', views.searchuser, name='searchuser'),
                path('id_card_page/<int:user_id>/', views.id_card_page, name='id_card_page'),

              ]
