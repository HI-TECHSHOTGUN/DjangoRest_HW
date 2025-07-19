from rest_framework import serializers

from materials.models import Lessons, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
