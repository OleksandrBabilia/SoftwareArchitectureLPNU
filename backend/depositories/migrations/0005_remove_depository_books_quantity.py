# Generated by Django 5.0.4 on 2024-05-05 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('depositories', '0004_rename_capacity_depository_books_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depository',
            name='books_quantity',
        ),
    ]
