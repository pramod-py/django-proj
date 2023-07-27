from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import os
from django.core.files.base import ContentFile

# Create your models here.


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    is_active = models.BooleanField(default=False)
    borrowed_book_status = models.BooleanField(default=False)
    borrowed_book_id = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'
 
    def save(self, *args, **kwargs):
       
        qr_code_data = f'{self.phone_number}${self.borrowed_book_id}'
        qrcode_img = qrcode.make(qr_code_data)
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.email.split("@")[0]}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
