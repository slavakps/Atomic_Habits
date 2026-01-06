from django.contrib.auth.models import User
from django.db import models

User.add_to_class('tg_chat_id', models.CharField(max_length=50, null=True, blank=True))
