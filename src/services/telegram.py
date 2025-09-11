import requests


def bot_set_webhook(token: str, webhook_url: str) -> tuple[bool, str]:
    url = f"https://api.telegram.org/bot{token}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    if response.status_code == 200:
        return True, ''
    return False, response.text
