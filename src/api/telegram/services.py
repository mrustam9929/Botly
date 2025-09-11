from api.telegram.bot_mapping import BOT_MAPPING
from apps.companies.models import CompanyBot


class BotService:
    @staticmethod
    def get_bot(bot_id: int):
        bot = CompanyBot.objects.filter(id=bot_id).first()
        if bot is None:
            raise Exception(f"Bot with id {bot_id} not found")
        bot_loader_class = BOT_MAPPING.get(bot.bot_module, None)
        if bot_loader_class is None:
            raise Exception(f"Bot module loader class {bot.bot_module} not found")
        return bot_loader_class(bot_id).get_bot()
