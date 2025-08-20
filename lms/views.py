from rest_framework.views import APIView
from rest_framework import status, viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Lesson, Subscription
from .paginators import LmsPaginator
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session


class OwnerAndModeratorPermissionsMixin:
    """
    Миксин для управления правами доступа и автоматического
    назначения владельца при создании объекта.
    """
    def get_queryset(self):
        """
        Фильтрует queryset:
        - для модераторов показывает все объекты.
        - для остальных пользователей - только их собственные.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name='moderators').exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Привязываем создаваемый объект к текущему пользователю."""
        serializer.save(owner=self.request.user)


class CourseViewSet(OwnerAndModeratorPermissionsMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LmsPaginator


class LessonViewSet(OwnerAndModeratorPermissionsMixin, viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LmsPaginator


class SubscriptionAPIView(APIView):
    """
    API для создания/удаления подписки на курс (переключатель).
        Принимает POST-запрос с `course_id`.
    - Если пользователь не подписан на курс - создает подписку.
    - Если пользователь уже подписан - удаляет подписку.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'Необходимо указать course_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Ищем подписку
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            message = 'Вы успешно отписались от курса.'
        else:
            message = 'Вы успешно подписались на курс.'

        return Response({'message': message}, status=status.HTTP_200_OK)

class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Создание платежа через Stripe.
    Принимает `course_id` для создания сессии оплаты.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Курс не найден.")

        amount = 1000.00

        stripe_product = create_stripe_product(course)
        stripe_price = create_stripe_price(stripe_product, amount)
        stripe_session = create_stripe_session(stripe_price)

        serializer.save(
            user=self.request.user,
            course=course,
            amount=amount,
            payment_method='card',
            stripe_session_id=stripe_session.id,
            stripe_payment_link=stripe_session.url
        )