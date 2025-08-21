from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Course, Lessons, Subscription


class LessonSubscriptionTestCase(APITestCase):

    def setUp(self):
        """Начальные данные для тестов"""
        self.user = User.objects.create(email="test@test.com", password="password")
        self.course = Course.objects.create(name="Тестовый курс", owner=self.user)
        self.lesson = Lessons.objects.create(
            name="Тестовый урок", course=self.course, owner=self.user
        )
        # Аутентифицируем клиента для всех последующих запросов
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {"name": "Новый урок", "course": self.course.pk}
        response = self.client.post(reverse("materials:lessons_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.count(), 2)

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse("materials:lessons_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в 'results' (из-за пагинации) есть один объект
        self.assertEqual(len(response.data.get("results")), 1)

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        data = {"name": "Обновленный урок"}
        response = self.client.patch(
            reverse("materials:lessons_update", kwargs={"pk": self.lesson.pk}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленный урок")

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(
            reverse("materials:lessons_delete", kwargs={"pk": self.lesson.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.count(), 0)

    def test_subscription(self):
        """Тестирование создания и удаления подписки"""
        data = {"course_id": self.course.pk}

        # Создаем подписку
        response = self.client.post(reverse("materials:subscriptions"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Удаляем подписку
        response = self.client.post(reverse("materials:subscriptions"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
