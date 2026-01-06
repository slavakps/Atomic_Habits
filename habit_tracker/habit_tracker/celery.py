import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

app = Celery("habit_tracker")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# периодический запуск задачи
app.conf.beat_schedule = {
    "send-habit-reminders-every-minute": {
        "task": "habits.tasks.send_habit_reminders",
        "schedule": crontab(),
    },
}
