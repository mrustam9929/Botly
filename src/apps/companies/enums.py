from django.db import models


class BotModules(models.TextChoices):
    FEEDBACK_BOT = 'FEEDBACK_BOT'


class BotMessageTypes(models.TextChoices):
    TEXT = 'TEXT'
    FILE = 'FILE'
    VOICE = 'VOICE'
    VIDEO = 'VIDEO'
    VOICE_VIDEO = 'VOICE_VIDEO'
