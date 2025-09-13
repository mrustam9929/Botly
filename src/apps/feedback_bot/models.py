from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.companies.enums import BotMessageTypes
from apps.companies.models import CompanyBot


class FbbSettings(models.Model):
    bot = models.ForeignKey(CompanyBot, on_delete=models.CASCADE, related_name='+')
    feedback_send_chat_ids = ArrayField(models.CharField(max_length=50), default=list)
    start_text = models.TextField(max_length=1000, default='')
    feedback_button_text = models.CharField(max_length=50, default='')
    feedback_create_button_text = models.CharField(max_length=50, default='')
    feedback_cancel_button_text = models.CharField(max_length=50, default='')
    feedback_send_text = models.TextField(max_length=1000, default='')
    allowed_message_types = ArrayField(models.CharField(max_length=50, choices=BotMessageTypes.choices), default=list)

    class Meta:
        db_table = "feedback_bot__settings"
        verbose_name = "Настройки бота"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"BOT: {self.bot.name} settings"



class FbbUser(models.Model):
    bot = models.ForeignKey(CompanyBot, on_delete=models.CASCADE, related_name='+')
    tg_id = models.BigIntegerField(db_index=True)
    phone = models.CharField(max_length=13, null=True)
    nickname = models.CharField(max_length=60, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'feedback_bot__users'
        unique_together = (('bot', 'tg_id'),)
        verbose_name = "Пользователи"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"BOT: {self.bot.name}"

class UserFeedBack(models.Model):
    user = models.ForeignKey(FbbUser, on_delete=models.CASCADE, related_name='feedbacks')
    tg_message_id = models.CharField(max_length=255, null=True)
    message_type = models.CharField(max_length=11, choices=BotMessageTypes.choices)
    text = models.TextField()
    file_id = models.CharField(max_length=255, null=True)
    video_id = models.CharField(max_length=255, null=True)


    class Meta:
        db_table = 'feedback_bot__users_feedback'
        verbose_name = "Отзывы"
        verbose_name_plural = verbose_name
