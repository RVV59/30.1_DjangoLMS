from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def deactivate_inactive_users():
    """
    Задача для деактивации пользователей, которые не заходили более 30 дней.
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)

    users_to_deactivate = User.objects.filter(last_login__lt=thirty_days_ago, is_active=True)

    count = users_to_deactivate.update(is_active=False)

    print(f"Deactivated {count} inactive users.")