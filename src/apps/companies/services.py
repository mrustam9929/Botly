from abc import ABC, abstractmethod

from telebot import TeleBot

from apps.companies.models import CompanyBot


class BotBuilder(ABC):
    def __init__(self, company_bot: CompanyBot):
        self.company_bot = company_bot

    def build(self):
        from telebot.storage import StateRedisStorage
        from telebot.handler_backends import RedisHandlerBackend
        from django.conf import settings
        bot = TeleBot(
            self.company_bot.token,
            parse_mode="HTML",
            state_storage=StateRedisStorage(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=1,
                prefix=f"bot:{self.company_bot.id}:state:"
            ),
            next_step_backend=RedisHandlerBackend(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=1,
                prefix=f"bot:{self.company_bot.id}:next:"
            ),
            reply_backend=RedisHandlerBackend(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=1,
                prefix=f"bot:{self.company_bot.id}::reply:"
            ),
            num_threads=1,
            skip_pending=True
        )

        self.register_handlers(bot)
        return bot

    @abstractmethod
    def register_handlers(self, bot: TeleBot):
        raise NotImplementedError