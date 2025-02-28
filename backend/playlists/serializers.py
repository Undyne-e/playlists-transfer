from rest_framework import serializers
from .models import YandexPlaylistTracks, YouTubePlaylistTracks

class PlaylistTransferSerializer(serializers.Serializer):
    source_platform = serializers.ChoiceField(choices=["spotify_music", "yandex_music", "deezer_music", "apple_music", "youtube_music"])
    target_platform = serializers.ChoiceField(choices=["spotify_music", "yandex_music", "deezer_music", "apple_music", "youtube_music"])
    playlist_uuid = serializers.CharField()

class YandexPlaylistTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = YandexPlaylistTracks
        fields = ['track_id', 'title', 'artist', 'album', 'duration']

class YouTubePlaylistTracksSerializer(serializers.ModelSerializer):
        class Meta:
            model = YouTubePlaylistTracks
            fields = ['track_id', 'title', 'artist', 'album', 'duration']
