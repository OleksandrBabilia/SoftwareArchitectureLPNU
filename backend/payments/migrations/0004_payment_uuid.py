# Generated by Django 5.0.4 on 2024-11-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_remove_payment_status_payment_success_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='uuid',
            field=models.UUIDField(default=2),
            preserve_default=False,
        ),
    ]
