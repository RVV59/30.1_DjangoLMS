from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Course, Lesson
from .permissions import IsModerator, IsOwner
from .serializers import (CourseSerializer, LessonSerializer,
                          MyTokenObtainPairSerializer)

class OwnerAndModeratorPermissionsMixin:
    """
    Миксин для управления правами доступа и автоматического
    назначения владельца при создании объекта.
    """
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Привязываем создаваемый объект к текущему пользователю."""
        serializer.save(owner=self.request.user)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class CourseViewSet(OwnerAndModeratorPermissionsMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(OwnerAndModeratorPermissionsMixin, viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

