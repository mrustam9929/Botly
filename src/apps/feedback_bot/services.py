from django.db.transaction import atomic

from apps.companies.enums import BotModules
from apps.companies.models import CompanyBot
from apps.feedback_bot.models import FbbSettings
from services.telegram import bot_set_webhook


class FeedBackBotService:

    @atomic
    def create_bot(self, company_id: int, name: str, _token: str):
        bot = CompanyBot.objects.create(
            company_id=company_id,
            bot_module=BotModules.FEEDBACK_BOT,
            name=name,
            _token=_token
        )
        bot_settings = FbbSettings.objects.create(
            bot=bot,
        )
        success, errors = bot_set_webhook(bot.token, bot.webhook_url)
        if not success:
            raise Exception(errors)
        return bot
