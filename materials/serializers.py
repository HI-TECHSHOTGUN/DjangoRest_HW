from rest_framework import serializers

from materials.models import Lessons, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, instance):
        return instance.lessons.count()
