import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_register_success():
    client = APIClient()

    url = reverse("register")

    data = {
        "username": "testuser",
        "password": "12345test",
    }

    response = client.post(url, data)

    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()
