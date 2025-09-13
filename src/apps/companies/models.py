from django.conf import settings
from django.db import models

from apps.companies.enums import BotModules
from services.security import token_cipher


class Company(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название компании',
        help_text='Уникальное имя компании (например, ООО "Альфа")'
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='companies',
        verbose_name='Владелец',
        help_text='Пользователь, создавший или управляющий этой компанией'
    )

    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name


class CompanyBot(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Компания',
        help_text='Компания, к которой принадлежит бот'
    )
    bot_module = models.CharField(
        choices=BotModules.choices,
        max_length=255,
        verbose_name='Модуль бота',
        help_text='Назначение или функциональность бота (например, жалобы, опросы и т.д.)'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя бота',
        help_text='Человекочитаемое имя бота для отображения в интерфейсе'
    )
    _token = models.CharField(
        max_length=255,
        verbose_name='Зашифрованный токен',
        help_text='Telegram токен бота (хранится в зашифрованном виде)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
        help_text='Дата и время создания записи'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлён',
        help_text='Дата и время последнего обновления'
    )

    class Meta:
        db_table = 'companies_bot'
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    @property
    def token(self) -> str:
        return token_cipher.decrypt(self._token)

    @token.setter
    def token(self, value):
        self._token = token_cipher.encrypt(value)

    @property
    def webhook_url(self) -> str:
        return f"{settings.TELEGRAM_WEBHOOK_URL}/{self.id}/"
