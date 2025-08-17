from rest_framework.routers import DefaultRouter
from .apps import LmsConfig
from .views import CourseViewSet, LessonViewSet



app_name = LmsConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = router.urls