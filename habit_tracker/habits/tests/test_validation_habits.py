import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.fixture
def auth_client(db):
    """
    Клиент с авторизованным пользователем
    """
    user = User.objects.create_user(username="validator", email="val@test.ru", password="12345test")

    client = APIClient()
    client.force_authenticate(user=user)

    return client, user


@pytest.mark.django_db
def test_cannot_set_reward_and_related_habit(auth_client):
    client, user = auth_client

    url = reverse("habits-list")

    habit_reward = Habit.objects.create(
        user=user,
        action="Смотреть сериал",
        time="20:00:00",
        place="дом",
        periodicity=1,
        duration=30,
        is_public=False,
        is_reward=True,
    )

    payload = {
        "action": "Читать книгу",
        "time": "21:00:00",
        "place": "дом",
        "periodicity": 1,
        "duration": 30,
        "is_public": False,
        "is_reward": False,
        "reward": "Пироженка",
        "related_habit": habit_reward.id,
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "reward" in response.data


@pytest.mark.django_db
def test_duration_cannot_be_more_than_120(auth_client):
    client, user = auth_client

    url = reverse("habits-list")

    payload = {
        "action": "Бегать",
        "time": "08:00:00",
        "place": "улица",
        "periodicity": 1,
        "duration": 300,
        "is_public": False,
        "is_reward": False,
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "duration" in response.data


@pytest.mark.django_db
def test_periodicity_min_value_1(auth_client):
    client, user = auth_client

    url = reverse("habits-list")

    payload = {
        "action": "Растяжка",
        "time": "09:00:00",
        "place": "дом",
        "periodicity": 0,
        "duration": 30,
        "is_public": False,
        "is_reward": False,
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "periodicity" in response.data
