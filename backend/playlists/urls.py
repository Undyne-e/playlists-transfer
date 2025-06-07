from django.urls import path
from .views import YandexSavePlaylistsView, YandexSaveTracksView, YouTubeSavePlaylistsView, YouTubeSaveTracksView, SpotifySavePlaylistsView, PlaylistTransferView, SpotifySaveTracksView

urlpatterns = [
    path("yandex/get_playlists/", YandexSavePlaylistsView.as_view(), name="yandex_playlists"),
    path("yandex/save_playlists/", YandexSaveTracksView.as_view(), name="yandex_tracks"),
    path("youtube/get_playlists/", YouTubeSavePlaylistsView.as_view(), name="youtube_playlists"),
    path("youtube/save_playlists/", YouTubeSaveTracksView.as_view(), name="youtube_tracks"),
    path("spotify/get_playlists/", SpotifySavePlaylistsView.as_view(), name="spotify_playlists"),
    path("spotify/save_playlists/", SpotifySaveTracksView.as_view(), name="spotify_tracks"),
    path("transfer/", PlaylistTransferView.as_view(), name="playlist_transfer"),

]