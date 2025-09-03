from django.db import models

from apps.companies.models import CompanyBot


class NaffUser(models.Model):
    tg_id = models.BigIntegerField()
    bot = models.ForeignKey(CompanyBot, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'naff_users'
