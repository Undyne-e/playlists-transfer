from django.urls import path
from .views import YandexSavePlaylistsView, YandexSaveTracksView

urlpatterns = [
    path("yandex/get_playlists/", YandexSavePlaylistsView.as_view(), name="yandex_playlists"),
    path("yandex/save_playlists/", YandexSaveTracksView.as_view(), name="yandex_tracks")
]