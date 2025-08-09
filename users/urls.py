from django.urls import path
from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    UserCreateAPIView,
    UserProfileAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    # --- НОВЫЙ URL ДЛЯ СПИСКА ПЛАТЕЖЕЙ ---
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),

    # --- Существующие или возможные URL для пользователей ---
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
]