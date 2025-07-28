from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from materials.models import Course, Lessons
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]
        else: # 'destroy'
            permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]



class LessonListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer


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


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
