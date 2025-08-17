from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_url_validator


class LessonInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description')


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[youtube_url_validator])
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons', 'is_subscribed')

    def get_is_subscribed(self, course):
        """
        Проверяет, подписан ли текущий пользователь на курс.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=course).exists()