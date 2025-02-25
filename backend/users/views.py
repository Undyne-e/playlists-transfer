#yandex
from .models import YandexToken

#google
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from .models import GoogleToken

#dj
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
from django.views import View
import requests

#env
from dotenv import load_dotenv
import os
load_dotenv()

@method_decorator(csrf_exempt, name='dispatch')
class YandexOAuthCallbackView(View):

    def get(self, request):

        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Код авторизации отсутствует"}, status=400)

        YANDEX_OAUTH_URL = "https://oauth.yandex.ru/token"
        YANDEX_REDIRECT_URI = "http://localhost:8000/auth/callback"

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": os.getenv("YANDEX_CLIENT_ID"),
            "client_secret": os.getenv("YANDEX_CLIENT_SECRET"),
            "redirect_uri": YANDEX_REDIRECT_URI,
        }
        token_data = requests.post(YANDEX_OAUTH_URL, data=payload).json()

        if "access_token" not in token_data:
            return JsonResponse(token_data, status=400)

        # Предположим, что пользователь уже аутентифицирован
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error": "Пользователь не аутентифицирован"}, status=401)

        # Сохраняем токен в базе данных
        YandexToken.objects.update_or_create(
            user=user,
            defaults={
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token'),
                'expires_in': token_data.get('expires_in'),
            }
        )

        return JsonResponse({"status": "success", "message": "Токен успешно сохранен"})
    

@method_decorator(csrf_exempt, name='dispatch')
class GoogleOAuthCallbackView(View):

    def post(self, request, *args, **kwargs):
        try:
            # Получение токена Djoser из заголовка
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Token '):
                return JsonResponse({'error': 'Token is required'}, status=401)

            token = auth_header.split(' ')[1]  # Извлечение токена

            # Поиск пользователя по токену
            try:
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)

            # Получение данных из JSON-запроса
            data = json.loads(request.body)
            code = data.get('code')

            if not code:
                return JsonResponse({'error': 'Code is required'}, status=400)

            # Настройка OAuth-потока
            CLIENT_SECRETS_FILE = './client_secret.json'
            SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri='http://localhost:5173/googlecallback'
            )

            # Обмен кода на токены
            flow.fetch_token(code=code)

            # Получение токенов
            creds = flow.credentials
            access_token = creds.token
            refresh_token = creds.refresh_token

            # Сохранение токенов для пользователя
            GoogleToken.objects.update_or_create(
                user=user,
                defaults={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            )

            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)