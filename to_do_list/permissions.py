from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, NotFound


class MyOwnPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated is False:
            raise NotFound
        
        return True

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        raise NotAuthenticated
