from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from apps.feedback_bot.models import FbbSettings



def get_actions(bot_settings: FbbSettings) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(bot_settings.confirm_button_text),
        KeyboardButton(bot_settings.cancel_button_text),

    )
    return markup