# Generated by Django 4.2.2 on 2023-07-28 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='number_of_books_borrowed',
            field=models.IntegerField(default=0),
        ),
    ]