# Generated by Django 4.2.2 on 2023-07-23 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_db_books_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_books',
            name='no_of_copies_current',
            field=models.IntegerField(default=1),
        ),
    ]
