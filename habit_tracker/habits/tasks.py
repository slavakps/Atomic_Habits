import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Habit


@shared_task
def send_habit_reminders():
    now = timezone.localtime(timezone.now())

    print("=== ЗАПУСК НАПОМИНАНИЯ ===")
    print("Текущее время:", now)
    print("Ищем привычки на:", now.hour, now.minute)

    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute, is_reward=False)

    print("Найдено привычек:", habits.count())

    for habit in habits:
        print("Отправляем напоминание по привычке:", habit.action)

        if not habit.user.tg_chat_id:
            print("⛔ у пользователя нет tg_chat_id")
            continue

        text = f"⏰ Напоминание\n\n" f"{habit.action}\n" f"{habit.place}"

        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": habit.user.tg_chat_id, "text": text},
        )
