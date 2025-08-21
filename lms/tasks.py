from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_course_update_email(user_email, course_title):
    """
    Задача для асинхронной отправки email об обновлении курса.
    """
    send_mail(
        subject=f'Обновление курса "{course_title}"',
        message=f'Курс "{course_title}", на который вы подписаны, был обновлен.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )