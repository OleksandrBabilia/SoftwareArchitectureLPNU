# Generated by Django 5.0.4 on 2024-11-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_rented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rented',
            field=models.BooleanField(default=False),
        ),
    ]
