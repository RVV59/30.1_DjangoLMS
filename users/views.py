from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter

# --- НОВОЕ ПРЕДСТАВЛЕНИЕ ДЛЯ СПИСКА ПЛАТЕЖЕЙ ---
class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода списка платежей с возможностью
    фильтрации и сортировки.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # Подключаем бэкенды для фильтрации и сортировки
    filter_backends = [DjangoFilterBackend]
    # Указываем наш кастомный класс фильтрации
    filterset_class = PaymentFilter


# --- Существующие или возможные представления для пользователей ---
# (Оставляю их здесь как пример, если у вас их еще нет)

class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для регистрации пользователя."""
    serializer_class = UserSerializer

class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Эндпоинт для управления профилем пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user