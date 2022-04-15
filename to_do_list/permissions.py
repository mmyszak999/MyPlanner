from re import T
from rest_framework import permissions

class MyOwnPermissions(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.owner == request.user:
            print(request.user)
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        return False