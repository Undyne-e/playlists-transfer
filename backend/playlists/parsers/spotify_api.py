from .base import BaseMusicAPI
import requests

class SpotifyAPI(BaseMusicAPI):

    def __init__(self, token):
        self.token = token

    def get_playlists(self):
        """Получение списка плейлистов пользователя."""
        url = 'https://api.spotify.com/v1/me/playlists'
        headers = {'Authorization': f'Bearer {self.token}'}
        response_data = requests.get(url=url, headers=headers).json()["items"]
        items=[]

        for item in response_data:
            playlist_id = item["id"]
            playlist_title = item["name"]
            track_count = item["tracks"]["total"]
            data = {
                "playlist_id": playlist_id,
                "title": playlist_title,
                "track_count": track_count,
            }
            items.append(data)
        return items




    def get_playlist_tracks(self, kind: int, playlist_id: str):
        """Получение треков из плейлиста."""
        pass

    def create_playlist(self, title: str):
        """Создание нового плейлиста."""
        pass

    def search_track(self, artist: str, title: str):
        pass

    def add_tracks_to_playlist(self, kind: int, track_id: int, album_id: int):
        """Добавление треков в плейлист."""
        pass