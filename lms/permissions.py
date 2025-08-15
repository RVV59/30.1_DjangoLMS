from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Права доступа для пользователей из группы 'moderators'.
    """
    message = 'Вы не являетесь модератором.'

    def has_permission(self, request, view):
        # Проверяем, состоит ли пользователь в группе 'moderators'
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """
    Права доступа для владельца объекта.
    """
    message = 'Вы не являетесь владельцем этого объекта.'

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False