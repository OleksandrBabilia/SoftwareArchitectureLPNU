from django.db import models
from authors.models import Author
from publishers.models import Publisher


class Ganre(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Ganre"
        verbose_name_plural = "Ganres"
        ordering = ["-name"]

    def __str__(self):
        return f"{self.name}" 


class Book(models.Model):
    title = models.CharField(max_length=55, db_index=True)
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    publication_date = models.DateField(db_index=True, null=True, blank=True)
    price = models.FloatField(db_index=True)
    author = models.ManyToManyField(Author)
    publisher= models.ForeignKey(Publisher, on_delete=models.DO_NOTHING)
    cover = models.ImageField(default='default_book_image.jpg', null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    page_count = models.PositiveSmallIntegerField()
    rating = models.FloatField()
    ganres = models.ManyToManyField(Ganre)
    rented = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-title"]

    def __str__(self):
        return f"{self.title}"

