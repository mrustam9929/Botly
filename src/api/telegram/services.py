from api.telegram.bot_mapping import BOT_MAPPING
from apps.companies.models import CompanyBot
from functools import lru_cache
from threading import RLock

_lock = RLock()

@lru_cache(maxsize=256)
def get_bot(pk: int):
    with _lock:
        company_bot = CompanyBot.objects.get(pk=pk, is_active=True)
        cls = BOT_MAPPING[company_bot.bot_module]
        bot_builder_cls = cls(company_bot)
        return bot_builder_cls.build()

