
from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    """
    Права доступа, которые разрешают действия владельцу объекта
    или персоналу (is_staff=True).
    """
    message = 'У вас нет прав для выполнения этого действия.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff