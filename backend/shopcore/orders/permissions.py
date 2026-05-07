from rest_framework.permissions import BasePermission


class IsAdminGroupUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        if request.method == 'GET' and 'user_id' in view.kwargs:
            return request.user.is_authenticated and request.user.id == int(view.kwargs['user_id'])

        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True

        if request.method == 'GET':
            return obj.orderPlacedByUserWithId == request.user.id or request.user.is_staff

        # Erlaube PUT, PATCH, DELETE nur für Admin-Benutzer
        return request.user.is_staff
