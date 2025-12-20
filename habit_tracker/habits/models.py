from django.db import models
from django.conf import settings

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    is_reward = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_to')
    reward = models.CharField(max_length=255, null=True, blank=True)
    periodicity = models.PositiveSmallIntegerField(default=1)
    duration = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action} ({self.user.username})"

