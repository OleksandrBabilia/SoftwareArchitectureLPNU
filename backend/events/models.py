from django.contrib.auth.models import User
from django.db import models
from depositories.models import Depository
from books.models import Book


class Event(models.Model):
    ARRIVAL = 'AR'
    DEPARTURE = 'DP'
    TRANSFER_FROM = 'TF'
    TRANSFER_TO = 'TO'
    
    EVENT_CHOICES = [
        (DEPARTURE, 'Departure'),
        (ARRIVAL, 'Arrival'),
        (TRANSFER_TO, 'Transfer from this to Another'),
        (TRANSFER_FROM, 'Transfer to this From Anothet'),
    ]
     
    event_type = models.CharField(max_length=2, choices=EVENT_CHOICES, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True) 
    related_depository = models.ForeignKey(Depository, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.event_type}-{self.responsible}" 


class EventDepository(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    depository = models.ForeignKey(Depository, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'depository')


class EventBook(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

