from rest_framework import serializers
from .models import User
# Payment,
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

#
# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'

class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичного просмотра профиля пользователя."""
    class Meta:
        model = User
        fields = ('id', 'email', 'city', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Переопределяем метод create, чтобы использовать create_user.
        Это гарантирует, что пароль будет правильно захеширован.
        """
        user = User.objects.create_user(**validated_data)
        return user
