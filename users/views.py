from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]

        return super().get_permissions()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
