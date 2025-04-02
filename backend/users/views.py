#yandex
from .models import YandexToken

#google
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from .models import GoogleToken

#spotify
from .models import SpotifyToken

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
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#env
import base64
from dotenv import load_dotenv
import os
load_dotenv()

class YandexOAuthCallbackView(APIView):
    """Обрабатывает код от Яндекса, проверяет Djoser-токен, получает access_token"""
    

    authentication_classes = [TokenAuthentication]  # Проверка Djoser-токена
    permission_classes = [IsAuthenticated]  # Разрешаем только аутентифицированным пользователям

    def get(self, request):

        # print("HEADERS:", request.headers) 
        # print("AUTH USER:", request.user)  

        # Получаем код из запроса
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No code provided"}, status=400)

        # Отправляем запрос на получение access_token Яндекса
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": os.getenv('YANDEX_CLIENT_ID'),
            "client_secret": os.getenv('YANDEX_CLIENT_SECRET'),
        }
        response = requests.post("https://oauth.yandex.ru/token", data=data)
        response_data = response.json()

        if "access_token" in response_data:
            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            user = request.user
            YandexToken.objects.update_or_create(
                user = user,
                defaults={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            )

            return Response({"message": "Token saved successfully!", 'yandex_token': access_token})

        return Response(response_data, status=400)
    

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
            SCOPES = [
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/youtube.force-ssl',
            ]

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
                'google_token': access_token,
                'refresh_token': refresh_token,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class SpotifyOAuthCallbackView(APIView):
    """Обрабатывает код от Spotify, проверяет Djoser-токен, получает access_token"""
    
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]  

    def post(self, request):

        data = json.loads(request.body)
        code = data.get('code')
        if not code:
            return Response({"error": "No code provided"}, status=400)
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:5173/spotifycallback",
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': f"Basic {encoded_credentials}", 
        }

        response_data = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers).json()

        if "access_token" in response_data:
            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            expires_in = response_data["expires_in"]
            user = request.user
            SpotifyToken.objects.update_or_create(
                user = user,
                defaults={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'expires_in': expires_in,
                }
            )

            print(1)
            return Response({"message": "Token saved successfully!", 'spotify_token': access_token})

        return Response(response_data, status=400)
