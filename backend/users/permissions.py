from django.db.models.fields import return_None
from rest_framework import permissions
from django.contrib.auth.models import Group
from urllib3 import request


class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Manager' group to access.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        manager_group = Group.objects.get(name='Manager')
        return manager_group in request.user.groups.all()


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Manager' group to access.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return False

class IsStuffUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow viewing for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow updates or deletes only for superusers
        return request.user.is_stuff or request.user.is_superuser
