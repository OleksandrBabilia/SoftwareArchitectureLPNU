from django.contrib.admin.utils import pretty_name
from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin
from .models import Book 


class BookManyToManyInline(admin.TabularInline):
    model = Book.author.through
    extra = 0


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class BookAdmin(ImportExportActionModelAdmin):
    list_display = ["title", "isbn", "publication_date", "price", "image_tag",]
    # list_select_related = ["author__first_name", "author__last_name", "publisher__name"]
    list_filter = ["title", "isbn", "publication_date", "price",]
    # inlines = [BookGanreInline]
    search_fields = ["title",]

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:80px"/>'.format(obj.cover.url))

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser: 
            return Book.objects.using('default').all()
        elif user.groups.filter(name='Manager').exists():
            return Book.objects.using('manager').all()
        else:
            return Book.objects.using('consultant').all()

