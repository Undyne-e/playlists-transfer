from rest_framework import serializers
from .models import YandexPlaylistTracks, YouTubePlaylistTracks, SpotifyPlaylistTracks

class PlaylistTransferSerializer(serializers.Serializer):
    source_platform = serializers.ChoiceField(choices=["spotify", "yandex_music", "youtube_music"])
    target_platform = serializers.ChoiceField(choices=["spotify", "yandex_music", "youtube_music"])
    playlist_uuid = serializers.CharField()

class YandexPlaylistTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = YandexPlaylistTracks
        fields = ['track_id', 'title', 'artist', 'album', 'duration']

class YouTubePlaylistTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubePlaylistTracks
        fields = ['track_id', 'title', 'artist', 'album', 'duration']

class SpotifyPlaylistTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyPlaylistTracks
        fields = ['track_id', 'title', 'artist', 'album', 'duration']