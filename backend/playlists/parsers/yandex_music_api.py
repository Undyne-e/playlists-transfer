from yandex_music import Client
from .base import BaseMusicAPI

class YandexMusicAPI(BaseMusicAPI):

    def __init__(self, token):
        self.token = token
        self.client = Client(self.token).init()

    def get_playlists(self):
        playlists = self.client.users_playlists_list()
        return playlists
    
    def get_playlist_tracks(self, kind: int,  playlist_id: str):
        playlist = self.client.users_playlists(kind, playlist_id)
        tracks = playlist.tracks
        return tracks

    def create_playlist(self, name: str, description: str):
        pass

    def add_tracks_to_playlist(self, playlist_id: str, tracks: list):
        pass