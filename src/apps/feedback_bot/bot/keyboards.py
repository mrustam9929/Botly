from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from apps.feedback_bot.models import FbbSettings


def get_main_keyboard(bot_settings: FbbSettings) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(bot_settings.feedback_create_button_text))
    return markup