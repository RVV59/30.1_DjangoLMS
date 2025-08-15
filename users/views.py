from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, PaymentSerializer, UserSerializer, UserPublicSerializer
from .permissions import IsOwnerOrStaff


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Определяем права доступа в зависимости от действия.
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrStaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения access и refresh токенов."""
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    # Платежи могут смотреть только авторизованные пользователи
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        Возвращает разный сериализатор в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            # Для просмотра списка или одного профиля - публичный
            return UserPublicSerializer
        # Для всех остальных действий (create, update) - полный
        return UserSerializer

    def get_permissions(self):
        """
        Регистрация (create) доступна всем.
        Остальные действия - только авторизованным.
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()