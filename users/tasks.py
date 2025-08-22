from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили в систему более 30 дней.
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=thirty_days_ago
    )

    count = inactive_users.count()

    if count > 0:
        inactive_users.update(is_active=False)
        logger.info(f"Успешно деактивировано {count} пользователей.")
    else:
        logger.info("Не найдено пользователей для деактивации.")

    return f"Проверка завершена. Деактивировано: {count}."