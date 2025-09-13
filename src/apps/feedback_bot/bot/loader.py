import telebot

from apps.companies.services import BotBuilder
from apps.feedback_bot.bot.handlers import main


class FeedbackBotBuilder(BotBuilder):

    def register_handlers(self, bot: telebot.TeleBot):
        main.register(bot, self.company_bot)
