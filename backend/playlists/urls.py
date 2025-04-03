from django.urls import path, include
from .views import YandexSavePlaylistsView, YandexSaveTracksView, YouTubeSavePlaylistsView, YouTubeSaveTracksView, SpotifySavePlaylistsView, PlaylistTransferViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'playlist-transfer', PlaylistTransferViewSet, basename='playlist-transfer')

urlpatterns = [
    path("yandex/get_playlists/", YandexSavePlaylistsView.as_view(), name="yandex_playlists"),
    path("yandex/save_playlists/", YandexSaveTracksView.as_view(), name="yandex_tracks"),
    path("youtube/get_playlists/", YouTubeSavePlaylistsView.as_view(), name="youtube_playlists"),
    path("youtube/save_playlists/", YouTubeSaveTracksView.as_view(), name="youtube_tracks"),
    path("spotify/get_playlists/", SpotifySavePlaylistsView.as_view(), name="spotify_playlists"),
    path('', include(router.urls)),

]