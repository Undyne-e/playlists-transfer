

from .serializers import *
from django.http import JsonResponse
from django.views import View
from users.oauth_providers import exchange_yandex_code_for_token

class YandexOAuthCallbackView(View):
    """Обрабатывает OAuth-коллбэк от Яндекса"""

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Код авторизации отсутствует"}, status=400)

        token_data = exchange_yandex_code_for_token(code)

        if "access_token" in token_data:
            return JsonResponse(token_data)
        else:
            return JsonResponse(token_data, status=400)

