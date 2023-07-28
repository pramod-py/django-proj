from django.db import models
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import os
import random


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RackName(models.Model):
    rack_number = models.IntegerField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
# class BookId(models.Model):
#     book_id = models.UUIDField(default=uuid.uuid4, editable=False)
#
#     def __str__(self):
#         return str(self.book_id.hex)[:10]
    
def generate_unique_book_id():
    while True:
        book_id = random.randint(1000000000, 9999999999)
        if not DB_Books.objects.filter(book_id=book_id).exists():
            return book_id


class DB_Books(models.Model):
    # book_id = models.OneToOneField(BookId, on_delete=models.CASCADE, primary_key=True, related_name='db_book')

    book_id = models.PositiveIntegerField(unique=True, default=generate_unique_book_id, editable=False)
    book_title = models.CharField(max_length=120)
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    categories = models.ManyToManyField(Category)
    publish_date = models.DateTimeField(default=timezone.now) # need to change default
    number_of_copies = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    book_language = models.CharField(max_length=20)
    book_price = models.IntegerField(default=1000)
    description = models.TextField(default='temp')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True)
    book_qr_code = models.ImageField(upload_to='book_qr_code/', blank=True)
    publisher = models.CharField(max_length=100, default='temp')
    isbn = models.CharField(max_length=20, default='temp')
    rating = models.IntegerField(default=5)
    reviews = models.TextField(default='temp')
    availability = models.CharField(max_length=20)
    rack_number = models.ManyToManyField(RackName)
    no_of_copies_actual = models.IntegerField(default=1) # This column contains the total no. of copies of each book that were initially present.
    no_of_copies_current = models.IntegerField(default=1) # This column contains the total no. of copies of each book that were currently available.


    def __str__(self):
        categories = ', '.join(category.name for category in self.categories.all())
        sub_categories = ', '.join(sub_category.name for sub_category in self.sub_category.all())
        return f'{self.book_title} {self.book_id} Categories: {categories} Subcategories: {sub_categories} Status: {self.status}'

        # return f'{self.book_title} {self.book_id} {self.categories.name} {self.sub_category.name} {self.status}'
    
    def save(self, *args, **kwargs):
        # self.no_of_copies_current = int(self.no_of_copies_actual)
        # if self.no_of_copies_current > 0:
        #     self.status = True  # Set status as True if there are available copies
        #     self.availability = 'Available'
        # else:
        #     self.status = False  # Set status as False if there are no available copies
        #     self.availability = 'Not Available'

        # Save Default QR Code
        if not self.book_qr_code:
            qr_code_data = f'{self.book_id}${self.book_title}'
            qrcode_img = qrcode.make(qr_code_data)
            canvas = Image.new('RGB', (290, 290), 'white')
            canvas.paste(qrcode_img)
            fname = f'{self.book_id}_{self.book_title}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.book_qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if the user has a QR code image and delete it
        if self.book_qr_code:
            file_path = Path(self.book_qr_code.path)
            if file_path.exists():
                file_path.unlink()
        super().delete(*args, **kwargs)


class Borrower_Details(models.Model):
    borrower_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(DB_Books, on_delete=models.CASCADE)
    borrowed_from_date = models.DateTimeField(default=timezone.now)
    borrowed_to_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    # issued_by = models.ForeignKey(Librarian, on_delete=models.CASCADE)

    def __str__(self):
        return f'Borrower ID: {self.Borrower_ID} - Book ID: {self.Book_ID}'

    def save(self, *args, **kwargs):
        if not self.borrowed_to_date:
            # Set the default value for Borrowed_To_Date (e.g., 30 days from the current date)
            self.borrowed_to_date = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

"""
Borrower_Details:

This table contains the details of all the persons who lent a book from the library. Each Student will be given a Unique borrower ID. All the library related activity for a particular person will be captured based on the Borrower ID. This table will be used to track the borrowing records. The borrower ID will serve as a primary key here.

Columns:

Borrower_ID: Unique ID given to each Student.

Book_ID: This column contains the book ID which was give to the borrower.

Borrowed_From_Date: The date on which the book was given a particular borrower.

Borrowed_To_Date: The date on which that book was supposed to be returned back or should be renewed.

Actual_Return_date: The date on which the borrower returned the book to the library.

Issued_by: The ID of the Librarian who issued book to the borrower.

"""
