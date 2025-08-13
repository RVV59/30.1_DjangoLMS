from django.urls import path
from rest_framework.routers import DefaultRouter
from .apps import LmsConfig
from .views import CourseViewSet, LessonViewSet, MyTokenObtainPairView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
] + router.urls # И добавляем все пути, сгенерированные роутером