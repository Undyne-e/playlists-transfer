from django.urls import path
from .views import YandexOAuthCallbackView, GoogleOAuthCallbackView, SpotifyOAuthCallbackView

urlpatterns = [
    path("auth/yandex_callback/", YandexOAuthCallbackView.as_view(), name="yandex_oauth_callback"),
    path("auth/google_callback/", GoogleOAuthCallbackView.as_view(), name="google_oauth_callback"),
    path("auth/spotify_callback/", SpotifyOAuthCallbackView.as_view(), name="spotify_oauth_callback"),
]
