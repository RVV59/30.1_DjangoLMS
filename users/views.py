from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment, User
from .filters import PaymentFilter
from .permissions import IsOwnerOrStaff
from .serializers import (
    MyTokenObtainPairSerializer,
    PaymentSerializer,
    UserSerializer,
    UserPublicSerializer
)


class PaymentListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка платежей с фильтрацией."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения access и refresh токенов."""
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    - Позволяет регистрацию всем.
    - Управляет правами доступа (владелец или персонал).
    - Динамически выбирает сериализатор для разных действий.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        Возвращает разный сериализатор в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            return UserPublicSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Определяем права доступа в зависимости от действия.
        """
        if self.action == 'create':
            # Регистрация доступна всем
            self.permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Редактировать, смотреть и удалять может владелец или персонал
            self.permission_classes = [IsOwnerOrStaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
