from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.companies.enums import BotMessageTypes
from apps.companies.models import CompanyBot


class FbbSettings(models.Model):
    bot = models.ForeignKey(
        CompanyBot,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Бот',
        help_text='Выберите бота, к которому относятся эти настройки'
    )
    feedback_send_chat_ids = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        verbose_name='Чаты для уведомлений',
        help_text='Введите chat_id через запятую, куда будут отправляться отзывы'
    )
    start_text = models.TextField(
        max_length=1000,
        default='Здравствуйте! Оставьте, пожалуйста, жалобу или предложение.',
        verbose_name='Текст приветствия',
        help_text='Сообщение, которое бот отправляет пользователю после команды /start'
    )
    feedback_send_message = models.TextField(
        max_length=1000,
        default='Хотите добавить ещё сообщение? Просто отправьте его. Готовы отправить отзыв? Нажмите ✅ Подтвердить или ❌ Отменить.',
        verbose_name='Текст при отправке отзыва',
        help_text='Сообщение пользователю после успешной отправки отзыва'
    )
    allowed_message_types = ArrayField(
        base_field=models.CharField(max_length=50, choices=BotMessageTypes.choices),
        default=list,
        verbose_name='Разрешённые типы сообщений',
        help_text='Выберите, какие типы сообщений разрешено отправлять (текст, фото, видео и т.д.)'
    )
    invalid_message_type_text = models.CharField(
        max_length=50,
        default='Неподдерживаемый тип сообщения.',
        verbose_name='Текст при недопустимом типе сообщения',
        help_text='Ответ пользователю, если он отправил запрещённый тип сообщения'
    )
    confirm_button_text = models.CharField(
        max_length=50,
        default='✅ Подтвердить',
        verbose_name='Текст кнопки подтверждения',
        help_text='Текст кнопки для подтверждения отзыва'
    )
    cancel_button_text = models.CharField(
        max_length=50,
        default='❌ Отменить',
        verbose_name='Текст кнопки отмены',
        help_text='Текст кнопки для отмены отзыва'
    )
    invalid_feedback_message_text = models.CharField(
        max_length=50,
        default='Вы ещё не отправили ни одного сообщения.',
        verbose_name='Текст при ошибке отправки отзыва',
        help_text='Сообщение, если пользователь нажал подтвердить без ввода данных'
    )
    feedback_confirm_text = models.TextField(
        max_length=1000,
        default='Спасибо! Ваше сообщение отправлено и будет рассмотрено.',
        verbose_name='Текст после подтверждения',
        help_text='Ответ пользователю после подтверждения отправки отзыва'
    )
    feedback_cancel_text = models.TextField(
        max_length=1000,
        default='Ваш отзыв отменён. Вы можете начать заново.',
        verbose_name='Текст после отмены',
        help_text='Ответ пользователю после отмены отзыва'
    )

    class Meta:
        db_table = "feedback_bot__settings"
        verbose_name = "Настройки бота"
        verbose_name_plural = "Настройки ботов"

    def __str__(self):
        return f"BOT: {self.bot.name} — настройки"


class FbbUser(models.Model):
    bot = models.ForeignKey(
        CompanyBot,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Бот',
        help_text='Бот, в котором зарегистрирован пользователь'
    )
    tg_id = models.BigIntegerField(
        db_index=True,
        verbose_name='Telegram ID',
        help_text='Уникальный идентификатор пользователя в Telegram'
    )
    phone = models.CharField(
        max_length=13,
        null=True,
        verbose_name='Телефон',
        help_text='Телефон пользователя, если был предоставлен'
    )
    nickname = models.CharField(
        max_length=60,
        null=True,
        verbose_name='Username',
        help_text='Username (никнейм) пользователя в Telegram'
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Имя',
        help_text='Имя пользователя, полученное из Telegram'
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя, полученная из Telegram'
    )

    class Meta:
        db_table = 'feedback_bot__users'
        unique_together = (('bot', 'tg_id'),)
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} (bot: {self.bot.name})"

class UserFeedBack(models.Model):
    user = models.ForeignKey(
        FbbUser,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Пользователь',
        help_text='Пользователь, отправивший отзыв'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name='Родительское сообщение',
        help_text='Если это ответ на другое сообщение — выберите родительское'
    )
    tg_message_id = models.CharField(
        max_length=255,
        null=True,
        verbose_name='ID сообщения в Telegram',
        help_text='ID сообщения в Telegram, если доступен'
    )
    message_type = models.CharField(
        max_length=11,
        choices=BotMessageTypes.choices,
        verbose_name='Тип сообщения',
        help_text='Тип содержимого отзыва (текст, фото, видео и т.д.)'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст сообщения пользователя (если есть)'
    )
    file_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='File ID',
        help_text='file_id вложения (фото, видео, документ и т.д.), если есть'
    )

    class Meta:
        db_table = 'feedback_bot__users_feedback'
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        preview = self.text.strip().replace('\n', ' ')[:30] + ('...' if len(self.text) > 30 else '')
        return f"Отзыв от {self.user.first_name or self.user.tg_id}: {preview}"
