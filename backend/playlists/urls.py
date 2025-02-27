from django.urls import path, include
from .views import YandexSavePlaylistsView, YandexSaveTracksView, PlaylistTransferViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'playlist-transfer', PlaylistTransferViewSet, basename='playlist-transfer')

urlpatterns = [
    path("yandex/get_playlists/", YandexSavePlaylistsView.as_view(), name="yandex_playlists"),
    path("yandex/save_playlists/", YandexSaveTracksView.as_view(), name="yandex_tracks"),
    path('', include(router.urls)),

]