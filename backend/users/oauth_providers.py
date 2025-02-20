import requests
from dotenv import load_dotenv
import os
load_dotenv()

YANDEX_OAUTH_URL = "https://oauth.yandex.ru/token"
YANDEX_REDIRECT_URI = "http://localhost:8000/auth/callback"

def exchange_yandex_code_for_token(code):
    """Обмен кода на OAuth-токен Яндекса."""
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("YANDEX_CLIENT_ID"),
        "client_secret": os.getenv("YANDEX_CLIENT_SECRET"),
        "redirect_uri": YANDEX_REDIRECT_URI,
    }
    response = requests.post(YANDEX_OAUTH_URL, data=payload)
    return response.json()
