from django.db import models


class BotModules(models.TextChoices):
    FEEDBACK_BOT = 'FEEDBACK_BOT'


class BotMessageTypes(models.TextChoices):
    TEXT = 'text'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    PHOTO = 'photo'
    VIDEO = 'video'
    VIDEO_NOTE = 'video_note'
    VOICE = 'voice'

