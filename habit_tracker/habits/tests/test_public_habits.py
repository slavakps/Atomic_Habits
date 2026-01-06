import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
def test_public_habits_available_without_auth():
    """
    Публичные привычки доступны без токена
    и приватные не попадают в выдачу
    """

    user = User.objects.create_user(username="user1", email="u1@test.ru", password="12345test")

    Habit.objects.create(
        user=user,
        action="Бегать по утрам",
        time="09:00:00",
        place="улица",
        periodicity=1,
        duration=20,
        is_public=True,
        is_reward=False,
    )

    Habit.objects.create(
        user=user,
        action="Медитация",
        time="22:00:00",
        place="дом",
        periodicity=1,
        duration=10,
        is_public=False,
        is_reward=False,
    )

    client = APIClient()

    url = reverse("public-habits-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["action"] == "Бегать по утрам"
