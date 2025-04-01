from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .base import BaseMusicAPI
from typing import List, Dict

class YouTubeMusicAPI(BaseMusicAPI):
    def __init__(self, token: str):
        creds = Credentials(token=token)
        self.client = build('youtube', 'v3', credentials=creds)

    def get_playlists(self) -> List[Dict]:
            request = self.client.playlists().list(
                part="snippet",
                mine=True
            )
            response = request.execute()
            return response.get("items", [])

    def get_playlist_tracks(self, kind: int, playlist_id: str) -> List[Dict]:
        tracks = []
        next_page_token = None

        while True:
            request = self.client.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,  # Максимальное разрешённое API значение
                pageToken=next_page_token
            )
            response = request.execute()

            # Проверка на наличие элементов
            items = response.get("items", [])
            if not items:
                break

            for item in items:
                snippet = item.get("snippet", {})
                if not snippet:
                    continue  # Если snippet нет, пропускаем элемент

                artist = snippet.get("videoOwnerChannelTitle", "Unknown")
                if artist[-8:] == " - Topic": artist = artist[:-8]
                track = {
                    "id": snippet["resourceId"].get("videoId", ""),
                    "title": snippet.get("title", "Unknown"),
                    "artist": artist,  # Берём канал как исполнителя
                    "album": "Unknown",  # YouTube не даёт информации об альбоме напрямую
                    "duration": 0  # Длительность можно получить через videos().list()
                }
                tracks.append(track)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return tracks



    def create_playlist(self, title: str) -> str:
        request = self.client.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": "Создано через API"},
                "status": {"privacyStatus": "private"}
            }
        )
        response = request.execute()
        return response["id"]

    def search_track(self, artist: str, title: str) -> Dict:
        query = f"{artist}-{title}"
        request = self.client.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        return response["items"][0] if response.get("items") else None

    def add_tracks_to_playlist(self, kind: int, playlist_id: str, track_id: str):
        request = self.client.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": track_id["id"]["videoId"]
                    }
                }
            }
        )
        request.execute()