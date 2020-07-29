from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == 'POST' or
            request.user and
            request.user.is_authenticated
        )