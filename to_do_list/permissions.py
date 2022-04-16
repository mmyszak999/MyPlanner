from rest_framework import permissions

class MyOwnPermissions(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print('0')
            return True
        
        return False


    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            print('1')
            return True
        
        return False