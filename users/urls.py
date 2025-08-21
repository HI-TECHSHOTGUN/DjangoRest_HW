from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from .views import PaymentViewSet, UserViewSet, PaymentCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
] + router.urls
