from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import YandexToken
from django.views import View
from .oauth_providers import exchange_yandex_code_for_token

class YandexOAuthCallbackView(View):
    """Обрабатывает OAuth-коллбэк от Яндекса"""

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Код авторизации отсутствует"}, status=400)

        token_data = exchange_yandex_code_for_token(code)

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