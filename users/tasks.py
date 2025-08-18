from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def block_inactive_users():
    """Блокировщик не активных поьзователей"""
    month_ago = timezone.now() - timedelta(days=30)
    users_to_block = User.objects.filter(last_login__lt=month_ago, is_active=True, is_superuser=False)

    count = users_to_block.update(is_active=False)
    print(f'Заблокировано {count} неактивных пользователей.')