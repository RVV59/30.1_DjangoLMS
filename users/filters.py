import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
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
        fields = ('paid_course', 'paid_lesson', 'payment_method',)