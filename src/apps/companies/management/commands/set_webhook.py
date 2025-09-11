from django.conf import settings
from django.core.management.base import BaseCommand

from apps.companies.models import CompanyBot
from services.telegram import bot_set_webhook


class Command(BaseCommand):
    help = "Устанавливает вебхук для Telegram-бота"

    def handle(self, *args, **kwargs):
        bot_id = input("Введите ID Бота")
        bot = CompanyBot.objects.get(id=bot_id)
        success, error_message = bot_set_webhook(bot.token, bot.webhook_url)
        if success:
            self.stdout.write(self.style.SUCCESS("Вебхук успешно установлен!"))
        else:
            self.stderr.write(error_message)
