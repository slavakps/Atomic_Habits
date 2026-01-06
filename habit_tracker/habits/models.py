from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    is_reward = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_to'
    )
    reward = models.CharField(max_length=255, null=True, blank=True)
    periodicity = models.PositiveSmallIntegerField(default=1)
    duration = models.PositiveSmallIntegerField(help_text="Время выполнения в секундах")
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action} ({self.user.username})"

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно заполнить вознаграждение и связанную привычку.")

        if self.is_reward and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")
