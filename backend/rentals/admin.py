from django.contrib import admin

# Admin for Rental Model
class RentalAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "approved", "rental_date", "return_date", "is_returned", "reserved"]
    list_filter = ["approved", "rental_date", "return_date", "is_returned", "reserved"]
    search_fields = ["book__title", "user__username"]
    list_editable = ["approved", "reserved"]  # Allows toggling approval status directly
    ordering = ["-rental_date"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        elif user.groups.filter(name='Manager').exists():
            return qs.filter(approved=True)  # Managers see approved rentals
        return qs.filter(user=user)  # Non-managers see their own rentals
