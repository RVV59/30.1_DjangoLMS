from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from lms.models import Course, Lesson # Важный импорт из другого приложения

# --- Кастомный менеджер для модели User ---
class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, где email является уникальным идентификатором
    для аутентификации вместо username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('Поле Email должно быть установлено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# --- Кастомная модель User ---
class User(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

# --- НОВАЯ МОДЕЛЬ: Платежи (Payment) ---
class Payment(models.Model):
    """
    Модель для хранения информации о платежах.
    """
    # Способы оплаты
    PAYMENT_METHOD_CASH = 'cash'
    PAYMENT_METHOD_TRANSFER = 'transfer'
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, 'Наличные'),
        (PAYMENT_METHOD_TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')

    # Платеж может быть либо за курс, либо за урок, поэтому делаем поля необязательными
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок')

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f'Платеж от {self.user} на сумму {self.amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'