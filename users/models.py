from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import os
from django.core.files.base import ContentFile
from pathlib import Path
from django.utils import timezone
# Create your models here.


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='user_qr_code', blank=True)
    is_active = models.BooleanField(default=False)
    borrowed_book_status = models.BooleanField(default=False)
    borrowed_book_id = models.CharField(max_length=20, default='00')
    number_of_books_borrowed = models.IntegerField(default=0)
    joined_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'
 
    # def save(self, *args, **kwargs):
    #
    #     qr_code_data = f'{self.phone_number}${self.borrowed_book_id}'
    #     qrcode_img = qrcode.make(qr_code_data)
    #     canvas = Image.new('RGB', (290, 290), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'{self.phone_number}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)

    # '''Logic working for update details'''
    # def save(self, *args, **kwargs):
    #     # Check if the model instance already exists in the database (i.e., it has an id)
    #     if self.id:
    #         # Retrieve the previous user object from the database
    #         try:
    #             previous_user_obj = Users.objects.get(id=self.id)
    #         except Users.DoesNotExist:
    #             # If the previous user object does not exist, set previous_qr_code to None
    #             previous_qr_code = None
    #         else:
    #             # Get the previous QR code image associated with the previous user object
    #             previous_qr_code = previous_user_obj.qr_code
    #
    #         # Check if the phone_number or borrowed_book_id has changed
    #         if not previous_qr_code or self.phone_number != previous_user_obj.phone_number:
    #             # If the phone_number or no previous QR code exists, create a new QR code
    #             qr_code_data = f'{self.phone_number}${self.borrowed_book_id}'
    #             qrcode_img = qrcode.make(qr_code_data)
    #             canvas = Image.new('RGB', (290, 290), 'white')
    #             canvas.paste(qrcode_img)
    #             buffer = BytesIO()
    #             canvas.save(buffer, 'PNG')
    #             self.qr_code.save(f'{self.phone_number}.png', File(buffer), save=False)
    #             canvas.close()
    #
    #             # Delete the previous QR code image if it exists
    #             if previous_qr_code:
    #                 previous_qr_code.delete()
    #
    #     # Save the updated model instance
    #     super().save(*args, **kwargs)
    # final logic for qr_code save if not if yes dont do anything
    def save(self, *args, **kwargs):

        # Condition to check user status is_active
        if self.number_of_books_borrowed > 0:
            self.is_active = True
        else:
            self.is_active = False

        # Check if the user already has a QR code image
        if not self.qr_code:
            # Create a new QR code for new users
            qr_code_data = f'{self.phone_number}${self.borrowed_book_id}'
            qrcode_img = qrcode.make(qr_code_data)
            canvas = Image.new('RGB', (350, 350), 'white')
            canvas.paste(qrcode_img)
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(f'{self.phone_number}.png', File(buffer), save=False)
            canvas.close()

        # Call the parent class's save() method to save the user instance
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if the user has a QR code image and delete it
        print(self.qr_code)
        print(self.qr_code.path)
        if self.qr_code:
            print('inside iof')
            file_path = Path(self.qr_code.path)
            if file_path.exists():
                file_path.unlink()
        super().delete(*args, **kwargs)

