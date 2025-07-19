from django.urls import path, include
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

app_name = MaterialsConfig.name
router = DefaultRouter()
router.register("course", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_detail"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path(
        "lessons/delete/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lessons_delete",
    ),
] + router.urls
