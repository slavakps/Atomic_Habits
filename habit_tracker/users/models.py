from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tg_chat_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
