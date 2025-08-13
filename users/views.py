from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter

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