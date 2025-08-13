from rest_framework import serializers
from .models import Payment, User

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


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
