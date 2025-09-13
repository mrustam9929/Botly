from django.core.management import CommandError
from django.core.management.base import BaseCommand

from api.telegram.services import get_bot
from apps.companies.models import CompanyBot

class Command(BaseCommand):
    help = "Запускает бота в режиме polling для локального теста"

    def add_arguments(self, parser):
        parser.add_argument("bot_id", type=int, help="ID бота в таблице TelegramBot")

    def handle(self, *args, **options):
        bot_id = options["bot_id"]

        try:
            db_bot = CompanyBot.objects.get(pk=bot_id)
        except CompanyBot.DoesNotExist:
            raise CommandError(f"Бот с id {bot_id} не найден")

        self.stdout.write(f"▶️ Запускаем бота '{db_bot.name}' (mode: polling)")

        bot = get_bot(bot_id)
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=30,
        )