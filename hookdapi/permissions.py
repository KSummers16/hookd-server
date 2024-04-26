from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if hasattr(request.user, "customer"):
            return request.user.customer.is_admin
        return False
