"""
Custom permissions for objects.
"""

from rest_framework.permissions import BasePermission


class AccessOwnerOnly(BasePermission):
    """Allow access just for the owner of the object."""

    def has_object_permission(self, request, view, obj):
        """Check if the request is made by the owner."""

        return obj.user.id == request.user.id
