from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription
from config import settings


@shared_task
def send_course_update_email(course_id):
    """Отправка email когда курс обновился"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        for sub in subscriptions:
            send_mail(
                subject=f'Обновление курса: {course.name}',
                message=f'Курс "{course.name}", на который вы подписаны, был обновлен.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.user.email],
                fail_silently=False,
            )
    except Course.DoesNotExist:
        print(f'Извините что-то пошло не так')