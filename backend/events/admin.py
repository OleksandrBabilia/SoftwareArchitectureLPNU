from django.contrib import admin
from django.db.models.fields import related_descriptors
from django.db import transaction

from depositories.models import Depository, BookDepository
from .models import Event, EventDepository, EventBook
from import_export.admin import ImportExportActionModelAdmin


class EventBookInline(admin.TabularInline):
    model = EventBook 
    extra = 0
    

class EventAdmin(ImportExportActionModelAdmin):
    list_display = ["event_type", "responsible", "timestamp", "id", "related_depository"]
    list_filter = ["event_type", "responsible", "timestamp", "related_depository"] 
    inlines = [EventBookInline]
    search_fields = ["event_type",]
    
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser: 
            return Event.objects.using('default').all()
        elif user.groups.filter(name='Manager').exists():
            return Event.objects.using('manager').all()
        else:
            return Event.objects.using('consultant').all()

    @transaction.atomic
    def add_book_quantity(self, book_id, depository_id, new_quantity, quantity):
        BookDepository.objects.update_or_create(
            book_id=book_id,
            depository_id=depository_id,
            defaults = {
                "quantity": quantity + new_quantity,
            }
        )

    @transaction.atomic
    def subtract_book_quantity(self, book_id, depository_id, new_quantity, quantity):
        BookDepository.objects.update_or_create(
            book_id=book_id,
            depository_id=depository_id,
            defaults = {
                "quantity": quantity - new_quantity,
            }
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print(obj) 
        try:
            query_books = EventBook.objects.filter(event=obj)
            books_ids = {book.book_id: book.quantity for book in query_books} # All book ids from event 

            query_depositories = EventDepository.objects.filter(event_id=obj.id).all()
            depository_ids = [depository.depository_id for depository in query_depositories] # Dep of Event 
            print(depository_ids) 
            query_depositories_books = BookDepository.objects.filter(depository_id=depository_ids[0]).values()
            depositories_books = {el["book_id"]: el["quantity"] for el in query_depositories_books} # All book ids from dep

            if obj.event_type == Event.ARRIVAL: 
                for book, quantity in books_ids.items():
                    self.add_book_quantity(book, depository_ids[0], quantity, depositories_books.get(book, 0))
            elif obj.event_type == Event.DEPARTURE:
                for book, quantity in books_ids.items():
                    self.subtract_book_quantity(book, depository_ids[0], quantity, depositories_books.get(book, 0))
            elif obj.event_type == Event.TRANSFER_FROM:
                related_depository_id = Depository.objects.filter(name=obj.related_depository).first()

                query_related_depositories_books = BookDepository.objects.filter(depository_id=related_depository_id.id).values()
                related_depositories_books = {el["book_id"]: el["quantity"] for el in query_related_depositories_books} # All book ids from dep
                for book, quantity in books_ids.items():
                    self.subtract_book_quantity(book, depository_ids[0], quantity, depositories_books.get(book, 0))
                
                for book, quantity in books_ids.items():
                    self.add_book_quantity(book, related_depository_id.id, quantity, related_depositories_books.get(book, 0))
            elif obj.event_type == Event.TRANSFER_TO:
                related_depository_id = Depository.objects.filter(name=obj.related_depository).first()

                query_related_depositories_books = BookDepository.objects.filter(depository_id=related_depository_id.id).values()
                related_depositories_books = {el["book_id"]: el["quantity"] for el in query_related_depositories_books} # All book ids from dep
                for book, quantity in books_ids.items():
                    self.add_book_quantity(book, depository_ids[0], quantity, depositories_books.get(book, 0))
                
                for book, quantity in books_ids.items():
                    self.subtract_book_quantity(book, related_depository_id.id, quantity, related_depositories_books.get(book, 0))
        except IndexError:
            pass
