import telebot
from django.conf import settings
from telebot.storage import StateRedisStorage

from apps.companies.services import BaseBotLoader

bot = telebot.TeleBot(
    settings.TG_BOT_TOKEN,
    state_storage=StateRedisStorage(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=1
    )
)


class FeedbackBotLoader(BaseBotLoader):

    def get_bot(self):
        return bot
