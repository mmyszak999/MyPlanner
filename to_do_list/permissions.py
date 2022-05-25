from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotFound


class MyOwnPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated is False:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        
        if request.user.is_staff or request.user.is_superuser:
            return True

        return False
