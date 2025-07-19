from rest_framework import viewsets
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
