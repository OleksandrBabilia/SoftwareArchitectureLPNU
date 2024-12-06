from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False  # Optional: set to False to prevent deletion of the profile through the user admin
    verbose_name_plural = 'Profile'  # Optional: change how it's labeled in the admin interface
    fields = ['premium']  # Include any other fields from Profile that you want to display


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]  # Add Profile inline to the User Admin

    # Specify which fields you want to display in the User Admin list view
    list_display = UserAdmin.list_display + ('get_premium_status',)  # Add `premium` field from Profile

    # Add a custom method to get premium status for display
    def get_premium_status(self, obj):
        return obj.profile.premium if hasattr(obj, 'profile') else False

    get_premium_status.short_description = 'Premium Status'  # This is the column title


# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

