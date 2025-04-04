from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class YandexPlaylists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    uid = models.IntegerField(blank=True, null=True)  
    playlist_uuid = models.CharField(max_length=255)  
    kind = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    track_count = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'playlist_uuid')  

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class YandexPlaylistTracks(models.Model):
    playlist = models.ForeignKey(YandexPlaylists, related_name='tracks', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(help_text="Длительность в секундах")

    def __str__(self):
        return f"{self.title} - {self.artist}"
    
class YouTubePlaylists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    playlist_id = models.CharField(max_length=255, unique=True)  # ID плейлиста в YouTube
    title = models.CharField(max_length=255)
    track_count = models.IntegerField(blank=True, null=True)  

    class Meta:
        unique_together = ('user', 'playlist_id')  

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class YouTubePlaylistTracks(models.Model):
    playlist = models.ForeignKey(YouTubePlaylists, related_name='tracks', on_delete=models.CASCADE)  
    track_id = models.CharField(max_length=255)  # ID трека в YouTube
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True, null=True, default="Unknown")
    duration = models.IntegerField(help_text="Длительность в секундах", blank=True, null=True)

    class Meta:
        unique_together = ('playlist', 'track_id')

    def __str__(self):
        return f"{self.title} - {self.artist}"
    

class SpotifyPlaylists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    playlist_id = models.CharField(max_length=255, unique=True) 
    title = models.CharField(max_length=255)
    track_count = models.IntegerField(blank=True, null=True)  

    class Meta:
        unique_together = ('user', 'playlist_id')  

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    

class SpotifyPlaylistTracks(models.Model):
    playlist = models.ForeignKey(SpotifyPlaylists, related_name='tracks', on_delete=models.CASCADE)  
    track_id = models.CharField(max_length=255)  # ID трека в YouTube
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True, null=True, default="Unknown")
    duration = models.IntegerField(help_text="Длительность в секундах", blank=True, null=True)

    class Meta:
        unique_together = ('playlist', 'track_id')

    def __str__(self):
        return f"{self.title} - {self.artist}"

