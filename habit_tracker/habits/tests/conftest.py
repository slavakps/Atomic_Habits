import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Неаутентифицированный клиент"""
    return APIClient()


@pytest.fixture
def auth_user(db):
    """Пользователь для тестов"""
    return User.objects.create_user(username="validator", email="validator@test.ru", password="12345test")


@pytest.fixture
def auth_client(api_client, auth_user):
    """Аутентифицированный клиент"""
    api_client.force_authenticate(user=auth_user)
    return api_client, auth_user
