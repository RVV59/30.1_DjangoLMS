import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    # Фильтр для сортировки по дате
    # Позволяет делать запросы ?ordering=payment_date и ?ordering=-payment_date
    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
        ),
        field_labels={
            'payment_date': 'Дата платежа',
        }
    )

    class Meta:
        model = Payment
        # Поля, по которым можно будет фильтровать напрямую
        # ?paid_course=1&payment_method=cash
        fields = ('paid_course', 'paid_lesson', 'payment_method',)