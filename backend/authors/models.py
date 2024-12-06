from django.db import models
from django.core.exceptions import ValidationError

class Author(models.Model):
    first_name = models.CharField(max_length=30, db_index=True)
    last_name = models.CharField(max_length=30, db_index=True)
    birthdate = models.DateField()
    nationality = models.CharField(max_length=75, db_index=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if Author.objects.filter(first_name=self.first_name, last_name=self.last_name).exists():
            raise ValidationError("Author with this first name and last name already exists.", code='author_exists')
        super().save(*args, **kwargs)

    def clean(self):
        if Author.objects.filter(first_name=self.first_name, last_name=self.last_name).exists():
            raise ValidationError("Author with this first name and last name already exists.", code='author_exists')

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["-first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

