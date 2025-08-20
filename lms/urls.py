from django.urls import path
from rest_framework.routers import DefaultRouter
from .apps import LmsConfig
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView, PaymentCreateAPIView



app_name = LmsConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]
urlpatterns += router.urls