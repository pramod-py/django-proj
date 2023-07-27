from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

from .models import DB_Books


class DB_BooksAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'book_id', 'get_categories', 'get_subcategories', 'status')
    list_filter = ('categories', 'sub_category', 'status')

    def get_categories(self, obj):
        return ', '.join(category.name for category in obj.categories.all())
    get_categories.short_description = 'Categories'

    def get_subcategories(self, obj):
        return ', '.join(sub_category.name for sub_category in obj.sub_category.all())
    get_subcategories.short_description = 'Subcategories'


admin.site.register(Author)
admin.site.register(DB_Books, DB_BooksAdmin)
# admin.site.register(BookId)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(RackName)
admin.site.register(Borrower_Details)

