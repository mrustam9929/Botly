import telebot
from telebot.types import Message

from apps.companies.models import CompanyBot
from apps.feedback_bot.bot import keyboards as kb
from apps.feedback_bot.models import FbbSettings


def register(bot: telebot.TeleBot, company_bot: CompanyBot, **kwargs):
    bot_settings = FbbSettings.objects.get(bot=company_bot)

    @bot.message_handler(commands=['start'], state="*")
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            bot_settings.start_text,
            reply_markup=kb.get_main_keyboard(bot_settings)
        )
