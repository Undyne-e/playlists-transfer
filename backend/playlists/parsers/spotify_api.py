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




    def get_playlist_tracks(self, kind: int, playlist_id: str, track_count: int):
        """Получение треков из плейлиста."""
        limit = 1
        offset = 0
        items = []
        headers = {'Authorization': f'Bearer {self.token}'}

        for item in range (track_count):
            url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}'
            response_data = requests.get(url=url, headers=headers).json()["items"][0]["track"]
            track_id = response_data["id"]
            title = response_data["name"]
            artist = response_data["artists"][0]["name"]
            album = response_data["album"]["name"]
            duration = response_data["duration_ms"]
            
            data = {
                "id": track_id,
                "title": title,
                "artist": artist,
                "album": album,
                "duration": duration,
            }
            items.append(data)
            offset+=1
        return items


    def create_playlist(self, title: str):
        """Создание нового плейлиста."""
        url = 'https://api.spotify.com/v1/me'
        headers = {'Authorization': f'Bearer {self.token}'}
        uid = requests.get(url=url, headers=headers).json()["id"]

        url = f'https://api.spotify.com/v1/users/{uid}/playlists'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        data = {
            "name": title,
            "description": "Создано через API",
        }
        playlist_id = requests.post(url=url, headers=headers, json=data).json()["id"]
        return playlist_id



    def search_track(self, artist: str, title: str):
        """Поиск трека."""
        url = "https://api.spotify.com/v1/search"
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            "q": f"track:{title} artist:{artist}",
            "type": "track",
            "limit": 1
        }   
        response_data = requests.get(url, headers=headers, params=params).json()
        tracks = response_data.get("tracks", {}).get("items", [])
        if tracks: return tracks[0]["id"]
        return None




    def add_tracks_to_playlist(self, kind: str, track_id: str, album_id: int):
        """Добавление треков в плейлист."""
        url = f'https://api.spotify.com/v1/playlists/{kind}/tracks'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        uris = [f'spotify:track:{track_id}']
        data = {"uris": uris}
        response = requests.post(url=url, headers=headers, json=data)
        return response
