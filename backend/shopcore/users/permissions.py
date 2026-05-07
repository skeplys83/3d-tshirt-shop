from rest_framework.permissions import BasePermission


class IsAdminGroupUser(BasePermission):
    def has_permission(self, request, view):
        # Erlaube POST für alle authentifizierten Benutzer (z.B. für Registrierung)
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        # Erlaube GET für authentifizierte Benutzer, wenn sie auf ihre eigene ID zugreifen
        if request.method == 'GET' and 'id' in view.kwargs:
            return request.user.id == int(view.kwargs['id']) or request.user.is_staff

        # Erlaube PUT/PATCH für den Benutzer selbst oder Admins
        if request.method in ['PUT', 'PATCH'] and 'id' in view.kwargs:
            return request.user.id == int(view.kwargs['id']) or request.user.is_staff

        # Erlaube DELETE nur für Admins
        if request.method in ['GET', 'DELETE']:
            return request.user.is_staff

        return False

    def has_object_permission(self, request, view, obj):
        # Erlaube PUT, PATCH nur für den Benutzer selbst oder Admins
        if request.method in ['PUT', 'PATCH']:
            return obj.id == request.user.id or request.user.is_staff

        # Erlaube DELETE nur für Admins
        if request.method == 'DELETE':
            return request.user.is_staff

        # Standard: Erlaube GET für den Benutzer selbst oder Admins
        return obj.id == request.user.id or request.user.is_staff
