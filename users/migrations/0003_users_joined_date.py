# Generated by Django 4.2.2 on 2023-07-28 17:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_number_of_books_borrowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='joined_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]