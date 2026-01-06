import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_user_login_success():

    client = APIClient()

    User.objects.create_user(username="tester", email="login@test.ru", password="12345test")

    url = reverse("login")

    response = client.post(url, {"username": "tester", "password": "12345test"}, format="json")

    assert response.status_code == 200
    assert "token" in response.data
    assert response.data["token"] != ""
