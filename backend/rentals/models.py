from django.db import models
from django.contrib.auth.models import User

from books.models import Book


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    rental_date = models.DateTimeField()  # Remove auto_now_add
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"
        ordering = ["-rental_date"]

    def __str__(self):
        return f"{self.user.username} rented {self.book.title}"
