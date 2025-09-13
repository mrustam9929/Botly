from django.conf import settings
from django.db import models

from apps.companies.enums import BotModules
from services.security import token_cipher


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='companies')
    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class CompanyBot(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bot_module = models.CharField(choices=BotModules.choices, max_length=255)
    name = models.CharField(max_length=255)
    _token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies_bot'
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    @property
    def token(self) -> str:
        return token_cipher.decrypt(self._token)

    @token.setter
    def token(self, value):
        self._token = token_cipher.encrypt(value)

    @property
    def webhook_url(self) -> str:
        return f"{settings.TELEGRAM_WEBHOOK_URL}/{self.id}/"
