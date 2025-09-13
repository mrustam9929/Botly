import telebot
from telebot.types import Message

from apps.companies.models import CompanyBot
from apps.feedback_bot.bot import keyboards as kb
from apps.feedback_bot.bot.states import States
from apps.feedback_bot.models import FbbSettings, FbbUser, UserFeedBack


def register(bot: telebot.TeleBot, company_bot: CompanyBot, **kwargs):
    bot_settings = FbbSettings.objects.get(bot=company_bot)

    @bot.message_handler(commands=["start"])
    def handle_start(message: Message):
        bot.send_message(
            message.chat.id,
            bot_settings.start_text,
        )
        bot.set_state(message.chat.id, States.feedback)
        bot.reset_data(message.chat.id)

    @bot.message_handler(state=States.feedback, func=lambda m: m.text == bot_settings.confirm_button_text)
    def handle_confirm(message: Message):

        with bot.retrieve_data(message.chat.id) as data:
            messages = data.get("messages", [])
            if not messages:
                bot.send_message(message.chat.id, bot_settings.invalid_feedback_message_text)
                return

            fbb_user, _ = FbbUser.objects.get_or_create(
                bot=company_bot,
                tg_id=message.chat.id,
                defaults=dict(
                    nickname=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                )
            )
            parent = None
            for msg in messages:
                feedback = UserFeedBack.objects.create(
                    user=fbb_user,
                    parent=parent,
                    tg_message_id=str(msg['tg_message_id']),
                    message_type=msg['message_type'],
                    text=msg['text'],
                    file_id=msg['file_id']
                )
                if parent is None:
                    parent = feedback

        bot.send_message(message.chat.id, bot_settings.feedback_confirm_text)
        bot.delete_state(message.chat.id)
        bot.reset_data(message.chat.id)
        handle_start(message)

    # Отмена
    @bot.message_handler(state=States.feedback, func=lambda m: m.text == bot_settings.cancel_button_text)
    def handle_cancel(message: Message):
        bot.send_message(message.chat.id, bot_settings.feedback_cancel_text)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.reset_data(message.from_user.id)
        handle_start(message)

    @bot.message_handler(state=States.feedback)
    def handle_feedback_content(message: Message):
        if message.content_type not in bot_settings.allowed_message_types:
            bot.send_message(message.chat.id, bot_settings.invalid_message_type_text)
            return

        with bot.retrieve_data(message.chat.id) as data:
            message_type = message.content_type
            file_id = None
            text = ""
            if message_type == "text":
                text = message.text
            elif message_type == "voice":
                file_id = message.voice.file_id
            elif message_type == "photo":
                file_id = message.photo[-1].file_id
            elif message_type == "video":
                file_id = message.video.file_id
            elif message_type == "document":
                file_id = message.document.file_id
            message_data = {
                "text": text,
                "file_id": file_id,
                "tg_message_id": message.message_id,
                "message_type": message.content_type,
            }
            data.setdefault("messages", []).append(message_data)
        bot.send_message(message.chat.id, bot_settings.feedback_send_message, reply_markup=kb.get_actions(bot_settings))

    # Подтверждение отправки
