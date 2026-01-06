import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


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
