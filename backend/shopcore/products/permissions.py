from rest_framework.permissions import BasePermission


class IsAdminGroupUser(BasePermission):
    def has_permission(self, request, view):
        # Erlaube andere Methoden (POST, PUT, DELETE) nur für is_staff Benutzer
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return request.user and request.user.is_authenticated and request.user.is_staff

        return False
