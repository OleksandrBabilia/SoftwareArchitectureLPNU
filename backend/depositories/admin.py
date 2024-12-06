from django.contrib import admin

from .models import BookDepository, Depository
from events.models import EventDepository
from import_export.admin import ImportExportActionModelAdmin
from events.admin import EventBookInline 


class BookDepositoryInline(admin.TabularInline):
    model = BookDepository
    extra = 0


class EventDepositorytInline(admin.TabularInline):
    model = EventDepository 
    extra = 0


class DepositoryAdmin(ImportExportActionModelAdmin):
    inlines = [BookDepositoryInline, EventDepositorytInline]
    list_display = ["name", "location", ]

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser: 
            return Depository.objects.using('default').all()
        elif user.groups.filter(name='Manager').exists():
            return Depository.objects.using('manager').all()
        else:
            return Depository.objects.using('consultant').all()


