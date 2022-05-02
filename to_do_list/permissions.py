from rest_framework import permissions, exceptions


class MyOwnPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated is False:
            raise exceptions.NotFound
        else:
            if request.user.is_staff or request.user.is_superuser:
                return True
            return True

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        raise exceptions.NotFound
