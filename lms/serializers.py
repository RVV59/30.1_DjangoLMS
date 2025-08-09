from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons')

    def get_lessons_count(self, course_instance):
        """Метод для получения количества уроков для конкретного курса."""
        return course_instance.lesson_set.count()
