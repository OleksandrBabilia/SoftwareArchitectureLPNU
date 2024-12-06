from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.utils.html import format_html
from .models import Payment

class PaymentAdmin(ImportExportActionModelAdmin):
    # Fields to display in the list view
    list_display = [
        "transaction_id",
        "payment_method",
        "amount",
        "success",
        "payment_date",
        "user",  # If the payment is linked to a user
    ]

    # Searchable fields
    search_fields = ["transaction_id", "payment_method", "success"]

    # Filtering options
    list_filter = ["payment_method", "success", "payment_date"]

    # Read-only fields for important information like `transaction_id`
    readonly_fields = ["transaction_id", "payment_date"]

    # You can also add inline editing if necessary for related models
    # inlines = [PaymentInline]

    # Customize the queryset based on the user (for example, show only payments of a certain group)
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return Payment.objects.all()
        elif user.groups.filter(name='Manager').exists():
            return Payment.objects.filter(success='Pending')  # Example: show only pending payments
        else:
            return Payment.objects.filter(user=user)  # Example: show payments for the logged-in user

    # Optional: If you want to display the success as a colored tag
    def success_tag(self, obj):
        if obj.success == "Completed":
            return format_html('<span style="color: green;">{}</span>', obj.success)
        elif obj.success == "Pending":
            return format_html('<span style="color: orange;">{}</span>', obj.success)
        else:
            return format_html('<span style="color: red;">{}</span>', obj.success)
    success_tag.short_description = "Payment success"

    # Optional: Show a formatted payment amount (e.g., with currency)
    def formatted_amount(self, obj):
        return format_html('<b>${}</b>', obj.amount)
    formatted_amount.short_description = "Amount"

    # Optionally customize the list view for pagination or rows
    list_per_page = 25  # Show 25 payments per page


# Register your models here
