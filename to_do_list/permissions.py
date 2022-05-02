from rest_framework import permissions, exceptions

from rest_framework.status import HTTP_404_NOT_FOUND

class Custom404(exceptions.APIException):
    status_code = HTTP_404_NOT_FOUND


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

        if request.user.is_superuser:
            return True
        
        return False