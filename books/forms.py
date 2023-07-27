from django import forms
from .models import DB_Books

class BookForm(forms.ModelForm):
    class Meta:
        model = DB_Books
        fields = '__all__'
