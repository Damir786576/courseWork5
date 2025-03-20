from celery import shared_task
from telegram import Bot
from django.conf import settings


@shared_task
def send_telegram_reminder(habit_id, chat_id):
    from .models import Habit
    habit = Habit.objects.get(id=habit_id)
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
    bot.send_message(chat_id=chat_id, text=message)
