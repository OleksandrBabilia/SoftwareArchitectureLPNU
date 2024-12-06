from django.db import models

from books.models import Book


class Depository(models.Model):
    name = models.CharField(max_length=55, db_index=True)
    location = models.CharField(max_length=125)
    
    class Meta:
        verbose_name = "Depository"
        verbose_name_plural = "Depositories"
        ordering = ["-name"]

    def __str__(self):
        return f"{self.name}" 


class BookDepository(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    depository = models.ForeignKey(Depository, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('book', 'depository')

