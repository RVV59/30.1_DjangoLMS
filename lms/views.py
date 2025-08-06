from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

# ViewSet для модели Course (обеспечивает полный CRUD)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Generic-классы для модели Lesson
class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока."""
    serializer_class = LessonSerializer

class LessonListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка уроков."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра одного урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока."""
    queryset = Lesson.objects.all()
