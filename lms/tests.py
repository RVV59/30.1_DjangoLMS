from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson, Subscription
from users.models import User

class LessonAndSubscriptionTestCase(APITestCase):
    def setUp(self):
        """Настройка тестовых данных перед каждым тестом."""
        self.user = User.objects.create(email='test@user.com', password='password')
        self.moderator = User.objects.create(email='moderator@user.com', password='password', is_staff=True)

        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)

        # ИСПРАВЛЕНО: Добавлено обязательное поле 'description'
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание для тестового урока.',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/test'
        )

    def test_lesson_list(self):
        """Тест получения списка уроков."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('lms:lessons-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_create_valid_url(self):
        """Тест создания урока с валидной ссылкой."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Новый урок',
            # ИСПРАВЛЕНО: Добавлено обязательное поле 'description'
            'description': 'Описание для нового урока.',
            'course': self.course.pk,
            'video_link': 'https://youtube.com/new_video'
        }
        response = self.client.post(reverse('lms:lessons-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title='Новый урок').exists())

    def test_lesson_create_invalid_url(self):
        """Тест создания урока с невалидной ссылкой."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок с плохой ссылкой',
            'description': 'Описание для урока с плохой ссылкой.',
            'course': self.course.pk,
            'video_link': 'https://vimeo.com/bad_video'
        }
        response = self.client.post(reverse('lms:lessons-list'), data=data)
        # ИСПРАВЛЕНО: Проверяем, что сервер вернул ошибку, как и ожидалось
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['video_link'][0], 'Разрешены ссылки только на youtube.com')

    def test_lesson_update_by_owner(self):
        """Тест обновления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Обновленный урок'}
        response = self.client.patch(reverse('lms:lessons-detail', args=[self.lesson.pk]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')

    def test_lesson_delete_by_owner(self):
        """Тест удаления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('lms:lessons-detail', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_subscription_toggle(self):
        """Тест создания и удаления подписки (переключатель)."""
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.pk}

        # 1. Подписываемся
        response = self.client.post(reverse('lms:subscribe'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы успешно подписались на курс.')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # 2. Проверяем статус в сериализаторе
        course_response = self.client.get(reverse('lms:courses-detail', args=[self.course.pk]))
        self.assertTrue(course_response.data['is_subscribed'])

        # 3. Отписываемся
        response = self.client.post(reverse('lms:subscribe'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы успешно отписались от курса.')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # 4. Проверяем статус снова
        course_response = self.client.get(reverse('lms:courses-detail', args=[self.course.pk]))
        self.assertFalse(course_response.data['is_subscribed'])