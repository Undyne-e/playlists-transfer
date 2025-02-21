from django.urls import path
from .views import YandexOAuthCallbackView

urlpatterns = [
    path("auth/callback/", YandexOAuthCallbackView.as_view(), name="yandex_oauth_callback"),
]
