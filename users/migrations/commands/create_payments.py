from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson
from decimal import Decimal

class Command(BaseCommand):
    """
    Кастомная команда для создания нескольких тестовых платежей.
    Запускается командой: python manage.py create_payments
    """
    help = 'Creates several test payments in the database'

    def handle(self, *args, **options):
        # Сначала очистим старые платежи, чтобы не создавать дубликаты при каждом запуске
        Payment.objects.all().delete()
        self.stdout.write(self.style.WARNING('Старые платежи удалены.'))

        # Найдем существующие объекты, за которые будем "платить"
        try:
            # Возьмем первого пользователя, первый курс и первый урок
            # В реальном проекте здесь может быть более сложная логика
            user = User.objects.first()
            course = Course.objects.first()
            lesson = Lesson.objects.last() # Возьмем последний урок для разнообразия

            if not user or not course or not lesson:
                self.stdout.write(self.style.ERROR('Недостаточно данных для создания платежей. Создайте хотя бы одного пользователя, курс и урок.'))
                return

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка при поиске объектов: {e}'))
            return

        # Список платежей, которые мы хотим создать
        payments_to_create = [
            {
                'user': user,
                'paid_course': course,
                'amount': Decimal('15000.00'),
                'payment_method': Payment.PAYMENT_METHOD_TRANSFER
            },
            {
                'user': user,
                'paid_lesson': lesson,
                'amount': Decimal('1200.50'),
                'payment_method': Payment.PAYMENT_METHOD_CASH
            },
            {
                'user': user,
                'paid_course': course,
                'amount': Decimal('14500.00'),
                'payment_method': Payment.PAYMENT_METHOD_CASH
            }
        ]

        # Создаем объекты в базе данных
        for payment_data in payments_to_create:
            Payment.objects.create(**payment_data)

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {len(payments_to_create)} платежей.'))
