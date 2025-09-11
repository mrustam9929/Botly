from apps.companies.enums import BotModules
from apps.feedback_bot.bot.loader import FeedbackBotBuilder

BOT_MAPPING = {
    BotModules.FEEDBACK_BOT: FeedbackBotBuilder
}
