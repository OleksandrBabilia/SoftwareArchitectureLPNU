from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        # Add other payment methods if needed
    ]
    uuid = models.UUIDField()
    success = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS,blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)  # Stored in cents
    payment_date = models.DateTimeField(blank=True, null=True)  # Make sure this field exists
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.payment_method} Payment - {self.transaction_id}'
