# Generated by Django 4.2.2 on 2023-07-19 03:15

import books.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RackName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rack_number', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.category')),
            ],
        ),
        migrations.CreateModel(
            name='DB_Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.PositiveIntegerField(default=books.models.generate_unique_book_id, editable=False, unique=True)),
                ('book_title', models.CharField(max_length=120)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('number_of_copies', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('book_language', models.CharField(max_length=20)),
                ('book_price', models.IntegerField(default=1000)),
                ('description', models.TextField(default='temp')),
                ('cover_image', models.ImageField(blank=True, upload_to='book_covers/')),
                ('book_qr_code', models.ImageField(blank=True, upload_to='book_qr_code/')),
                ('publisher', models.CharField(default='temp', max_length=100)),
                ('isbn', models.CharField(default='temp', max_length=20)),
                ('rating', models.IntegerField(default=5)),
                ('reviews', models.TextField(default='temp')),
                ('availability', models.CharField(max_length=20)),
                ('no_of_copies_actual', models.IntegerField(default=1)),
                ('no_of_copies_current', models.IntegerField()),
                ('book_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('categories', models.ManyToManyField(to='books.category')),
                ('rack_number', models.ManyToManyField(to='books.rackname')),
                ('sub_category', models.ManyToManyField(to='books.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Borrower_Details',
            fields=[
                ('borrower_id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed_from_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('borrowed_to_date', models.DateTimeField()),
                ('actual_return_date', models.DateTimeField(blank=True, null=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.db_books')),
            ],
        ),
    ]