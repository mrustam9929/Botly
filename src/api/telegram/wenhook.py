import json
import telebot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.telegram.services import get_bot
from core.settings import logger

@csrf_exempt
def webhook(request, pk):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            bot = get_bot(pk)
            bot.process_new_updates([telebot.types.Update.de_json(json_data)])
        except Exception as e:
            logger.error(e)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)
