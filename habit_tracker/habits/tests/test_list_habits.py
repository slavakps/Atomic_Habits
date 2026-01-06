import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
def test_user_sees_only_own_habits():

    client = APIClient()

    user1 = User.objects.create_user(username="user1", email="u1@test.ru", password="12345test")

    user2 = User.objects.create_user(username="user2", email="u2@test.ru", password="12345test")

    Habit.objects.create(
        user=user1,
        action="Читать книгу",
        time="10:00:00",
        place="дом",
        periodicity=1,
        duration=30,
        is_public=False,
        is_reward=False,
    )

    Habit.objects.create(
        user=user2,
        action="Бегать",
        time="08:00:00",
        place="улица",
        periodicity=1,
        duration=20,
        is_public=False,
        is_reward=False,
    )

    client.force_authenticate(user=user1)

    url = reverse("habits-list")

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1

    habit = response.data["results"][0]

    assert habit["action"] == "Читать книгу"
    assert habit["user"] == user1.id
