import telebot

from apps.companies.services import BotBuilder


class FeedbackBotBuilder(BotBuilder):

    def register_handlers(self, bot: telebot.TeleBot):
        pass
