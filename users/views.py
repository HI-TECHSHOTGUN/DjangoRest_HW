from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from .services import create_stripe_product, create_stripe_price, create_stripe_session


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]

        return super().get_permissions()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получаем курс из запроса
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)
        payment = Payment.objects.create(
            user=request.user, paid_course=course, amount=course.price
        )
        try:
            product_id = create_stripe_product(course.name)
            price_id = create_stripe_price(product_id, payment.amount)
            session_id, payment_link = create_stripe_session(price_id)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        payment.stripe_session_id = session_id
        payment.payment_link = payment_link
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
