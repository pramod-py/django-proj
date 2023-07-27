from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

# Register your models here.

# class UsersAdmin(UserAdmin):
#     # How data display in admin pannel
#     list_display = ('email', 'first_name', 'last_name', 'is_active',)
#     list_display_links = ('email', 'first_name', 'last_name', )
#     ordering = ('email',)
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

# admin.site.register(Users, UsersAdmin)
admin.site.register(Users)