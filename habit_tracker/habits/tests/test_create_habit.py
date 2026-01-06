import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_user_can_create_habit():
    """
    Пользователь может создать свою привычку
    """

    client = APIClient()

    user = User.objects.create_user(username="habituser", email="habit@test.ru", password="12345test")

    client.force_authenticate(user=user)

    url = reverse("habits-list")  # из HabitViewSet

    payload = {
        "action": "Утренняя зарядка",
        "time": "08:00:00",
        "is_public": False,
        "is_reward": False,
        "place": "дом",
        "periodicity": 1,
        "duration": 60,
    }

    response = client.post(url, payload, format="json")
    print(response.data)

    assert response.status_code == 201
    assert response.data["action"] == payload["action"]
    assert response.data["user"] == user.id
