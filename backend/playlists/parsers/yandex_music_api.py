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

    def create_playlist(self, title: str):
        playlist = self.client.users_playlists_create(title=title)
        return playlist
    
    def search_track(self, artist: str, title: str):
        result = self.client.search(f"{artist} - {title}", type_="track")

        if result.tracks and result.tracks.results:
            best_match = result.tracks.results[0]
            track_id = best_match.id
            album_id = best_match.albums[0].id if best_match.albums else None

            return track_id, album_id

        return None, None


    def add_tracks_to_playlist(self, kind: int, track_id: int, album_id: int):
        playlist = self.client.users_playlists(kind=kind)
        response = playlist.insert_track(track_id=track_id, album_id=album_id)
        return response