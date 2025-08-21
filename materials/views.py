from django.utils import timezone
from datetime import timedelta

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lessons, Subscription
from materials.paginators import MaterialsPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from .tasks import send_course_update_email


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsModerator | IsOwner]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        course = serializer.save()
        if course.last_update < timezone.now() - timedelta(hours=4):
            send_course_update_email.delay(course.id)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        if course.last_update < timezone.now() - timedelta(hours=4):
            send_course_update_email.delay(course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
