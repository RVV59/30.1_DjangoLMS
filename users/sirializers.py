from rest_framework import serializers
from .models import Payment, User

# Сериализатор для модели Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


# Сериализатор для модели User (может понадобиться для профиля и регистрации)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar')