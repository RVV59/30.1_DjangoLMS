from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter

class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода списка платежей с возможностью
    фильтрации и сортировки.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    # Указываем наш кастомный класс фильтрации
    filterset_class = PaymentFilter

# Задел на будущее
class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для регистрации пользователя."""
    serializer_class = UserSerializer

class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Эндпоинт для управления профилем пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user