from django_filters import rest_framework as filters
from .models import Payment

class PaymentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
        ),
        field_labels={
            'payment_date': 'Дата платежа',
        }
    )

    class Meta:
        model = Payment
        fields = {
            'paid_course': ['exact'],
            'paid_lessons': ['exact'],
            'payment_method': ['exact'],
        }