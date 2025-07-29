from django.apps import AppConfig
import os
import stripe


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        stripe.api_key = os.getenv('STRIPE_API_KEY')
